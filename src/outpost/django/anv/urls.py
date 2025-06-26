from django.urls import path

from . import views

app_name = "anv"

urlpatterns = [
    path(
        "station/<str:pk>",
        views.StationView.as_view(),
        name="station",
    ),
]
