from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from weatherapi.models import WeatherApiKey
from django.urls import reverse

from unittest.mock import patch


class WeatherApiKeyViewTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpassword'
        )

        # Create a WeatherApiKey instance for testing
        self.weather_api_key = WeatherApiKey.objects.create(
            user=self.user,
            weather_api_key='test_api_key'
        )

        # Create an APIClient for making requests
        self.client = APIClient()

        # Authenticate the client with the user's token
        self.client.force_authenticate(user=self.user)

    def test_weather_api_key_list_view_success(self):
        """Test listing weather API keys for the authenticated user."""
        response = self.client.get(reverse('weatherapi:key-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 
    
    def test_weather_api_key_list_unauthorized(self):
        """
        Test listing weather API keys for the unauthenticated user
        shoul return 401
        """
        client = APIClient()
        response = client.get(reverse('weatherapi:key-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_weather_api_key_view_success(self):
        """Test creating a new weather API key for the authenticated user."""
        data = {'weather_api_key': 'new_test_api_key'}
        response = self.client.post(reverse('weatherapi:create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WeatherApiKey.objects.filter(user=self.user).count(), 2)
    
    def test_create_weather_api_key_view_success(self):
        """
        Test creating a new weather API key for unauthenticated user
        should return 401
        """
        client = APIClient()
        data = {'weather_api_key': 'new_test_api_key'}
        response = client.post(reverse('weatherapi:create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('weatherapi.views.OpenWeatherApiRequests.get_city_coordinates')
    @patch('weatherapi.views.OpenWeatherApiRequests.get_city_temperature')
    def test_retrieve_weather_data_view_success(self, mock_coordinates, mock_temperature):
        """Test retrieving weather data for a city."""
        
        mock_coordinates.return_value = {'lat': 1, 'lon':2}
        mock_temperature.return_value = {'temperature': 10}
        
        response = self.client.get(reverse('weatherapi:weather', args=['tokyo']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        mock_coordinates.assert_called_once_with({'temperature': 10}, 'test_api_key')
        mock_temperature.assert_called_once_with('tokyo', 'test_api_key')
    
    @patch('weatherapi.views.OpenWeatherApiRequests.get_city_coordinates')
    def test_retrieve_weather_data_view_failure(self, mock_coordinates):
        """Test retrieving weather data for a nonexistent city."""
        mock_coordinates.side_effect = ValueError("Mocked error")
        
        response = self.client.get(reverse('weatherapi:weather', args=['non existent']))
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "City not found."})
        
        mock_coordinates.assert_called_once_with('non existent', 'test_api_key')


    def test_retrieve_weather_data_view_failure(self):
        """Test retrieve weather data for unauthenticated user should return 401"""
        client = APIClient()
        response = client.get(reverse('weatherapi:weather', args=['non existent']))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_retrieve_weather_data_view_failure(self):
        """Test retrieve weather data for user withou OpenWeather key should return 400"""
        user = get_user_model().objects.create_user(
            email='test2@test.com',
            password='testpassword'
        )
        
        client = APIClient()

        client.force_authenticate(user=user)
        response = client.get(reverse('weatherapi:weather', args=['tokyo']))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)