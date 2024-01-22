"""
Views for the Weather API
"""
from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response

from rest_framework.views import APIView

from weatherapi.serializers import WeatherApiKeySerializer
from .models import WeatherApiKey
from .api_requests import OpenWeatherApiRequests


class WeatherApiKeyListView(generics.ListAPIView):
    """List weather API keys for the authenticated user."""
    serializer_class = WeatherApiKeySerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve and return the weather API keys for the authenticated user
        user = self.request.user
        return WeatherApiKey.objects.filter(user=user)

class CreateWeatherApiKeyView(generics.CreateAPIView):
    """Create a new weather API key for the authenticated user."""
    serializer_class = WeatherApiKeySerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Access the authenticated user from the request
        user = self.request.user

        # Save the item with the user relationship
        serializer.save(user=user)


class RetrieveWeatharDataView(APIView):
    """Retrie data from the OpenWeatherAPI"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            city = self.kwargs.get('city')            
            user_api_key = WeatherApiKey.objects.filter(user=self.request.user).first()
            if not user_api_key:
                return Response({"error": "User does not have an api key for OpenWeather."},
                                status=status.HTTP_400_BAD_REQUEST)
            api_key = user_api_key.weather_api_key        

            open_weather_api = OpenWeatherApiRequests()
            
            city_info = open_weather_api.get_city_coordinates(city, api_key)
            temperature = open_weather_api.get_city_temperature(city_info, api_key)

            return Response(temperature, status=status.HTTP_200_OK)
        except IndexError as e:
            return Response({"error": "City not found."},
                            status=status.HTTP_400_BAD_REQUEST)
    