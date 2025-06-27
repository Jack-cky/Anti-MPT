from django.urls import path

from .executes import pipeline
from .views import dashboard


app_name = "anitmpt-dashboard"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("api/v1/update", pipeline, name="pipeline"),
]
