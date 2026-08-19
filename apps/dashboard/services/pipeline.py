from decimal import Decimal
from pathlib import Path

import pandas as pd
from django.conf import settings
from django.db import transaction
from django.db.models import DecimalField
from django.utils import timezone
from prefect import flow, get_run_logger, task

from antimpt.agents import AntiMPT
from antimpt.evaluation.backtest import take_positions
from antimpt.market import (
    consolidate_data,
    get_equities,
    get_market_index,
    get_risk_free,
)

from ..models import Dashboard


DECIMAL_FIELDS = {
    field.name: field.null
    for field in Dashboard._meta.fields
    if isinstance(field, DecimalField)
}


@task(name="Fetch equity data", retries=2, retry_delay_seconds=30)
def fetch_equity_data() -> pd.DataFrame:
    equity = get_equities(**settings.EQUITY, src="yfinance")[0]
    get_run_logger().info(f"Fetched equity data with {len(equity)} rows.")

    return equity


@task(name="Fetch benchmark data", retries=2, retry_delay_seconds=30)
def fetch_benchmark_data(
    equity: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    start, end = equity.index[[0, -1]].strftime("%Y-%m-%d")
    risk_free = get_risk_free(start, end, src="yfinance")
    mkt_idx = get_market_index(start, src="yfinance")
    get_run_logger().info(f"Fetched benchmark data from {start} to {end}.")

    return {"risk_free": risk_free, "mkt_idx": mkt_idx}


def create_agent(
    cfg_agent: dict[str, object],
    agents: list[dict[str, object]],
) -> AntiMPT:
    match algorithm := cfg_agent["algorithm"]:
        case "A2C" | "PPO" | "DQN":
            return AntiMPT(
                algorithm,
                artefact=[
                    algorithm,
                    cfg_agent["experiment"],
                    cfg_agent["snapshot"],
                ],
            )
        case "Ensemble":
            return AntiMPT(
                algorithm,
                agents=[
                    agent for agent in agents
                    if agent.get("algorithm") != "Ensemble"
                ],
            )
        case _:
            raise ValueError(f"Invalid algorithm: {cfg_agent['algorithm']}")


@task(name="Build agent inference results", retries=2, retry_delay_seconds=30)
def build_agent_dataframe(
    cfg_agent: dict[str, object],
    agents: list[dict[str, object]],
    equity: pd.DataFrame,
    benchmarks: dict[str, pd.DataFrame],
    created_at: pd.Timestamp,
) -> pd.DataFrame:
    agent = create_agent(cfg_agent, agents)
    algorithm = cfg_agent["algorithm"]
    histories = take_positions(agent, equity, render_mode="robot")

    df = consolidate_data(equity, histories, **benchmarks).assign(
        agent=algorithm,
        created_at=created_at,
    )
    get_run_logger().info(f"Built for {algorithm} with {len(df)} rows.")

    return df


def get_processed_data_path(dt: pd.Timestamp) -> Path:
    pth = Path(settings.REPO_ROOT) / "data" / "processed"
    pth.mkdir(parents=True, exist_ok=True)

    return pth / f"antimpt_{dt:%Y%m%dT%H%M%S}.parquet"


def build_records(
    df: pd.DataFrame,
    created_at: pd.Timestamp,
) -> list[Dashboard]:
    return [
        Dashboard(
            agent=row["agent"],
            trading_date=pd.Timestamp(row["trading_date"]).date(),
            created_at=created_at,
            **{
                field_name: (
                    None
                    if nullable and pd.isna(row.get(field_name))
                    else Decimal("0")
                    if pd.isna(row.get(field_name))
                    else Decimal(str(row.get(field_name)))
                )
                for field_name, nullable in DECIMAL_FIELDS.items()
            },
        )
        for row in df.to_dict("records")
    ]


def update_database(df: pd.DataFrame, created_at: pd.Timestamp) -> None:
    data = build_records(df, created_at)

    with transaction.atomic():
        Dashboard.objects.all().delete()
        Dashboard.objects.bulk_create(data, batch_size=1_000)


def cache_data(df: pd.DataFrame, pth_out: Path) -> None:
    pth_tmp = pth_out.with_suffix(f"{pth_out.suffix}.tmp")
    df.to_parquet(pth_tmp, index=False)
    pth_tmp.replace(pth_out)


@task(name="Persist database snapshot", retries=3, retry_delay_seconds=60)
def persist_snapshot(df: pd.DataFrame, created_at: pd.Timestamp) -> None:
    if df.empty:
        raise ValueError("No dashboard data was generated.")

    pth_out = get_processed_data_path(created_at)

    with transaction.atomic():
        update_database(df, created_at)
        transaction.on_commit(lambda: cache_data(df, pth_out))
    get_run_logger().info(f"Persisted database snapshot to {pth_out}.")


@flow(name="inference-workflow", retries=1, retry_delay_seconds=30)
def run_pipeline() -> None:
    dt_update = timezone.now()

    equity = fetch_equity_data()
    benchmarks = fetch_benchmark_data(equity)
    df = pd.concat([
        build_agent_dataframe(
            cfg_agent, settings.AGENTS, equity, benchmarks, dt_update,
        )
        for cfg_agent in settings.AGENTS
    ])
    persist_snapshot(df, dt_update)
