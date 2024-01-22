from django.test import TestCase
from django.contrib.auth import get_user_model
from weatherapi.models import WeatherApiKey

class WeatherApiKeyModelTest(TestCase):
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

    def test_weather_api_key_str(self):
        """Test the __str__ method of WeatherApiKey"""
        self.assertEqual(str(self.weather_api_key), 'test_api_key')

    def test_weather_api_key_user_relation(self):
        """Test the relationship between WeatherApiKey and User"""
        self.assertEqual(self.weather_api_key.user, self.user)

    def test_weather_api_key_max_length(self):
        """Test the max_length of weather_api_key field"""
        max_length = self.weather_api_key._meta.get_field('weather_api_key').max_length
        self.assertEqual(max_length, 200)
