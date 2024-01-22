"""
Customized django-admin
"""

from django.contrib import admin
from .models import WeatherApiKey
from django.utils.translation import gettext_lazy as _

class WeatherApiKeyAdmin(admin.ModelAdmin):
    list_display = ['user', 'weather_api_key']    

admin.site.register(WeatherApiKey, WeatherApiKeyAdmin)
