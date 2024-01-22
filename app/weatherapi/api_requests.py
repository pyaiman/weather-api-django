import os
import requests
from .helpers import get_country_alpha_3

from dotenv import load_dotenv

class OpenWeather:
    get_city_coordinates_url = "http://api.openweathermap.org/geo/1.0/direct?q=city_name&appid=api_key"
    weather_url = "https://api.openweathermap.org/data/2.5/weather?lat=city_lat&lon=city_lon&units=metric&appid=api_key"

class OpenWeatherApiRequests:
    def __init__(self) -> None:
        self.weather_url = OpenWeather.weather_url
        self.get_city_coordinates_url = OpenWeather.get_city_coordinates_url

    def get_city_coordinates(self, city_name, api_key):
        url = self.url_builder(
            url=self.get_city_coordinates_url,
            city_name=city_name,
            api_key=api_key)

        r = requests.get(url).json()[0]
            
        country_alpha_3 = get_country_alpha_3(r['country'])
        
        r['country'] = country_alpha_3
        
        return r


    def get_city_temperature(self, city, api_key):
        url = self.url_builder(
            url=self.weather_url,
            city_lat=str(city.get('lat')),
            city_lon=str(city.get('lon')),
            api_key=api_key
        )

        r = requests.get(url).json()

        result = {
            'city_name': city.get('name'),
            'country': city.get('country'),
            'min': r['main']['temp_min'],
            'max': r['main']['temp_max'],
            'feels_like': r['main']['feels_like'],            
        }      
        
        return result
    
    @staticmethod
    def url_builder(**kwargs) -> str:
        url = kwargs.pop('url')    
        for k, v in kwargs.items():
            url = url.replace(k, v)
        return url