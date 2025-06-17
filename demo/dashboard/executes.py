import pandas as pd
from django.conf import settings
from django.http import JsonResponse

from antimpt import AntiMPT
from antimpt.utils import take_positions, get_equities, consolidate_data
from dashboard.models import Dashboard


def update_database(df: pd.DataFrame) -> None:
    Dashboard.objects.all().delete()

    data_objects = [Dashboard(**rw) for _, rw in df.iterrows()]
    Dashboard.objects.bulk_create(data_objects, ignore_conflicts=True)


def pipeline(request) -> JsonResponse:
    agent = AntiMPT(settings.AGENT["algorithm"], artefact=settings.AGENT.values())

    equity = get_equities(*settings.EQUITY.values(), "yfinance")[0]
    histories = take_positions(agent, equity, render_mode="robot")

    df = consolidate_data(equity, histories, "yfinance")
    update_database(df)

    return JsonResponse({
        "status": 200,
        "message": "Commpleted",
    })
