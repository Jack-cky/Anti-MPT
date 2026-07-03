from datetime import datetime

import pandas as pd

from .benchmarks import get_market_index, get_risk_free


def consolidate_data(
    equity: pd.DataFrame,
    histories: list[dict[str, bool | float | int | str]],
    src: str = "cache",
) -> pd.DataFrame:
    equity = equity[["close"]].reset_index(names="date") \
        .rename(columns={"close": "price_close"})
    equity["date"] = equity["date"].dt.strftime("%Y-%m-%d")
    start, end = equity["date"].iloc[[0, -1]].values

    results = pd.DataFrame(histories)[["date", "action_taken", "portfolio"]]
    funds = results.at[0, "portfolio"]

    risk_free = get_risk_free(start, end, funds, src=src)
    mkt_idx = get_market_index(start, funds, src=src)

    df = equity.merge(results, on="date", how="left") \
        .merge(risk_free, on="date", how="left") \
        .merge(mkt_idx, on="date", how="left")

    df["trading_date"] = pd.to_datetime(df["date"])

    df["action"] = df["action_taken"].fillna("HOLD")
    df["price_long"] = df["price_close"].where(df["action"].isin(["LONG"]))
    df["price_short"] = df["price_close"].where(
        df["action"].isin(["SHORT", "CLOSE"]),
    )

    df[["portfolio", "risk_free"]] = df[["portfolio", "risk_free"]].ffill()

    df["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df.replace({float("nan"): None}, inplace=True)

    return df[[
        "trading_date", "price_close", "price_long",
        "price_short", "portfolio", "market_index",
        "risk_free", "created_at",
    ]]
