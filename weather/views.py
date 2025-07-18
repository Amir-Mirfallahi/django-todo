from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from decouple import config


class GetLatestWeatherApiView(APIView):
    permission_classes = [AllowAny]
    @method_decorator(cache_page(60 * 10))
    def get(self, request):
        api_key = config("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?lat=35.7219&lon=51.3347&lang=fa&appid={api_key}"
        response = requests.get(url)
        return Response({'data': response.json()})