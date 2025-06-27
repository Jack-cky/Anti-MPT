import pandas as pd
from django.conf import settings
from django.http import JsonResponse

from antimpt import AntiMPT
from antimpt.utils import consolidate_data, get_equities, take_positions
from dashboard.models import Dashboard


def update_database(df: pd.DataFrame) -> None:
    Dashboard.objects.all().delete()

    data_objects = [Dashboard(**rw) for _, rw in df.iterrows()]
    Dashboard.objects.bulk_create(data_objects, ignore_conflicts=True)


def pipeline(request) -> JsonResponse:
    if request.GET.get("secret") == settings.SECRET_PIPELINE:
        try:
            agent = AntiMPT(
                settings.AGENT["algorithm"],
                artefact=settings.AGENT.values(),
            )

            equity = get_equities(*settings.EQUITY.values(), "yfinance")[0]
            histories = take_positions(agent, equity, render_mode="robot")

            df = consolidate_data(equity, histories, "yfinance")
            update_database(df)
        except Exception:
            return JsonResponse({"status": "failed"})
    else:
        return JsonResponse({"status": "invalid secret"})

    return JsonResponse({"status": "commpleted"})
