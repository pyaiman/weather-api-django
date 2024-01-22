"""
URL mappings for the WeatherApi API.
"""
from django.urls import path
from weatherapi import views

app_name = 'weatherapi'

urlpatterns = [
    path('weather-api-key/', views.WeatherApiKeyListView.as_view(), name='key-list'),
    path('create/', views.CreateWeatherApiKeyView.as_view(), name='create'),
    path('weather/<str:city>', views.RetrieveWeatharDataView.as_view(), name='weather'),
]
