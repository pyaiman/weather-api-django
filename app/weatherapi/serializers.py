"""
Serializers for the Weather API View
"""

from .models import WeatherApiKey
from rest_framework import serializers

class WeatherApiKeySerializer(serializers.ModelSerializer):
    """Serializer for the weather api key object."""

    class Meta:
        model = WeatherApiKey
        fields = ['weather_api_key']
   
