"""Weather API model"""
from django.db import models
from django.conf import settings

class WeatherApiKey(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    weather_api_key = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.weather_api_key