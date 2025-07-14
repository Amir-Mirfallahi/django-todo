from .views import GetLatestWeatherApiView
from django.urls import path

app_name = 'weather'

urlpatterns = [
    path("", GetLatestWeatherApiView.as_view(), name="get-latest-weather"),
]