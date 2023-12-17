from django.urls import path
from airlines.airplanes.api import views as airplane_views


urlpatterns = [
    path(
        route="airplanes/",
        view=airplane_views.AirplaneList.as_view(),
        name="airplanes"
    ),
]