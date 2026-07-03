from django.urls import path

from .views import dashboard, health


app_name = "antimpt_dashboard"

urlpatterns = [
    path("health", health, name="health"),
    path("", dashboard, name="dashboard"),
]
