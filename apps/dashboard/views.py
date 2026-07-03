import pandas as pd
from django.conf import settings
from django.core.cache import cache
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render

from .models import Dashboard


SUMMARY_FIELDS = [
    "trading_date",
    "portfolio",
    "market_index",
    "risk_free",
    "created_at",
]
GRAPH_FIELDS = [
    "trading_date",
    "price_close",
    "price_long",
    "price_short",
    "portfolio",
    "market_index",
    "risk_free",
    "created_at",
]


def _get_empty_state_context() -> dict[str, bool]:
    return {
        "has_data": False,
    }


def _get_refresh_token() -> str:
    latest_update = Dashboard.objects.aggregate(
        last_update=Max("created_at")
    )["last_update"]

    if latest_update is None:
        return "empty"

    return latest_update.isoformat()


def _query_agent_records(agent: str, fields: list[str]) -> pd.DataFrame:
    queryset = (
        Dashboard.objects.filter(agent=agent)
        .order_by("trading_date")
        .values(*fields)
    )
    df = pd.DataFrame(list(queryset))

    if df.empty:
        return df

    df["trading_date"] = pd.to_datetime(df["trading_date"])
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"])

    for numeric_field in [
        "price_close",
        "price_long",
        "price_short",
        "portfolio",
        "market_index",
        "risk_free",
    ]:
        if numeric_field in df.columns:
            df[numeric_field] = pd.to_numeric(df[numeric_field])

    return df.reset_index(drop=True)


def _get_configured_agents() -> list[str]:
    return [agent["algorithm"] for agent in settings.AGENTS]


def _get_metadata() -> dict[str, object]:
    return {
        "configured_agents": _get_configured_agents(),
        "display_timezone": (
            "HKT" if settings.TIME_ZONE == "Asia/Hong_Kong"
            else settings.TIME_ZONE
        ),
    }


def _get_performance(df: pd.DataFrame) -> dict[str, float | str]:
    t0 = df["portfolio"].iat[0]
    tn = df["portfolio"].iat[-1]
    std = df["portfolio"].std()
    rf = df["risk_free"].iat[-1]

    sharpe_ratio = 0.0 if pd.isna(std) or std == 0 else (tn - rf) / std

    return {
        "funds": t0,
        "portfolio": tn,
        "return": (tn / t0 - 1) * 100,
        "sharpe_ratio": sharpe_ratio,
        "last_update": df["created_at"].iat[-1],
    }


def _get_agent_outperformance_count(df: pd.DataFrame) -> int:
    if "market_index" not in df.columns:
        return 0

    return int((df["portfolio"] > df["market_index"]).sum())


def _score_summary(
    summary: dict[str, float | str],
) -> tuple[float | str, float | str]:
    return summary["beats_market"], summary["return"]


def _get_best_agent_summary(
    summaries: list[dict[str, float | str]],
) -> dict[str, float | str] | None:
    if not summaries:
        return None

    return max(summaries, key=_score_summary)


def _build_agent_summaries() -> list[dict[str, float | str]]:
    summaries = []

    for agent in _get_configured_agents():
        agent_df = _query_agent_records(agent, SUMMARY_FIELDS)
        if agent_df.empty:
            continue

        summaries.append(
            {
                "agent": agent,
                "beats_market": _get_agent_outperformance_count(agent_df),
                **_get_performance(agent_df),
            }
        )

    return sorted(
        summaries,
        key=lambda summary: summary["portfolio"],
        reverse=True,
    )


def _get_cached_agent_summaries() -> list[dict[str, float | str]]:
    refresh_token = _get_refresh_token()
    cache_key = f"dashboard:agent-summaries:{refresh_token}"
    return cache.get_or_set(cache_key, _build_agent_summaries, 300)


def build_agent_graphs(agent: str) -> dict[str, str]:
    agent_df = _query_agent_records(agent, GRAPH_FIELDS)
    if agent_df.empty:
        return {}

    from antimpt.evaluation.interaction import get_interactive_graphs

    return get_interactive_graphs(agent_df)


def _get_cached_agent_graphs(agent: str) -> dict[str, str]:
    refresh_token = _get_refresh_token()
    cache_key = f"dashboard:agent-graphs:{agent}:{refresh_token}"

    return cache.get_or_set(cache_key, lambda: build_agent_graphs(agent), 300)


def _get_selected_agent_summary(
    summaries: list[dict[str, float | str]], requested_agent: str | None,
) -> dict[str, float | str] | None:
    if not summaries:
        return None

    if requested_agent is not None:
        for summary in summaries:
            if summary["agent"] == requested_agent:
                return summary

    return _get_best_agent_summary(summaries)


def _build_empty_context() -> dict[str, object]:
    return {
        **_get_metadata(),
        **_get_empty_state_context(),
    }


def _build_dashboard_context(
    agent_summaries: list[dict[str, float | str]],
    requested_agent: str | None,
) -> dict[str, object] | None:
    best_agent_summary = _get_best_agent_summary(agent_summaries)
    selected_agent_summary = _get_selected_agent_summary(
        agent_summaries,
        requested_agent,
    )

    if best_agent_summary is None or selected_agent_summary is None:
        return None

    return {
        "has_data": True,
        **selected_agent_summary,
        "selected_agent": selected_agent_summary["agent"],
        "best_agent": best_agent_summary["agent"],
        "agent_summaries": agent_summaries,
        "last_update": selected_agent_summary["last_update"],
        **_get_metadata(),
        **_get_cached_agent_graphs(selected_agent_summary["agent"]),
    }


def dashboard(request) -> render:
    agent_summaries = _get_cached_agent_summaries()
    empty_context = _build_empty_context()

    if not agent_summaries:
        return render(request, "dashboard/index.html", empty_context)

    context = _build_dashboard_context(
        agent_summaries,
        request.GET.get("agent"),
    )

    if context is None:
        return render(request, "dashboard/index.html", empty_context)

    return render(request, "dashboard/index.html", context)


def health(request) -> HttpResponse:
    return HttpResponse("ok", content_type="text/plain")


def error_404(request, exception) -> render:
    return render(request, "dashboard/404.html", status=404)


def error_500(request) -> render:
    return render(request, "dashboard/500.html", status=500)
