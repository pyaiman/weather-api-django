"""
Test for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'password@123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_normalized_email(self):
        """Test email normalization"""
        sample_emails = [
            ['test1@EXAMple.com', 'test1@example.com'],
            ['TEST1@EXAMPLE.com', 'TEST1@example.com'],
        ]

        for email, normalized_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'test123')
            self.assertEqual(user.email, normalized_email)

    def test_create_user_without_email(self):
        """Test create user without email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='password123')

    def test_create_superuser(self):
        """Test create a superuser."""
        email = 'superuser@example.com'
        password = 'password@123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
