import pandas as pd
from django.conf import settings
from django.shortcuts import render

from antimpt.utils import get_interactive_graphs
from .models import Dashboard


def query_latest_records() -> pd.DataFrame:
    return pd.DataFrame(list(Dashboard.objects.all().values()))


def get_metadata() -> dict[str, int|str]:
    return {
        "agent": settings.AGENT["algorithm"],
    }

def get_performance(df: pd.DataFrame) -> dict[str, int|str]:
    t0 = df["portfolio"].iat[0]
    tn = df["portfolio"].iat[-1]
    std = df["portfolio"].std()
    rf = df["risk_free"].iat[-1]

    return {
        "funds": t0,
        "portfolio": tn,
        "return": (tn / t0 - 1) * 100,
        "sharpe_ratio": (tn - rf) / std,
        "last_update": df["created_at"].iat[-1],
    }


def dashboard(request) -> render:
    df = query_latest_records()

    context = {
        **get_metadata(),
        **get_performance(df),
        **get_interactive_graphs(df),
    }

    return render(request, "index.html", context)


def error_404(request, exception) -> render:
    return render(request, "404.html", status=404)


def error_500(request) -> render:
    return render(request, "500.html", status=500)
