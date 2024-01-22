"""
Tests for the user views.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from user.serializers import UserSerializer

USER_PAYLOAD = {
    'email': 'test@test.com',
    'password': 'pass@123',
    'name': 'Test Name',
    }


def create_user(**params):
    """Create and return new user."""
    return get_user_model().objects.create_user(**params)

class UserViewTests(TestCase)    :
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test create user is successful."""      
        response = self.client.post(reverse('user:create'), USER_PAYLOAD)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=USER_PAYLOAD['email'])
        self.assertTrue(user.check_password(USER_PAYLOAD['password']))
        self.assertNotIn('password', response.data)

    def test_email_already_exists(self):
        """Test email already exists should return error"""        
        create_user(**USER_PAYLOAD)
        
        response = self.client.post(reverse('user:create'), USER_PAYLOAD)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class UserListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()        
        self.user = create_user(**USER_PAYLOAD)
        self.serialized_user = UserSerializer(self.user).data

    def test_user_list_view_success(self):
        """Test list users view."""
        response = self.client.get(reverse('user:user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn(self.serialized_user, response.data)


class UserDetailsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(**USER_PAYLOAD)

    def test_user_details_view_success(self):
        response = self.client.get(reverse('user:user-details', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Name')

    def test_user_details_view_failure(self):
        """Test get user that does not exist."""
        response = self.client.get(reverse('user:user-details', args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UserUpdateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(**USER_PAYLOAD)

    def test_user_update_view_success(self):
        data = {'name': 'Updated Name'}
        response = self.client.patch(reverse('user:user-update', args=[self.user.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')

    def test_user_update_view_failure(self):
        """Test update inexistent user."""
        self.client.force_authenticate(user=None)
        data = {'name': 'Updated Name'}
        response = self.client.patch(reverse('user:user-update', args=[999]), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UserDeleteViewTests(TestCase):
    def setUp(self):
        payload = {'email': 'superuser@test.com','password': 'pass@123',}
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(**payload)
        self.client.force_authenticate(user=self.user)
        
        self.user_to_be_deleted = create_user(**USER_PAYLOAD)

    def test_user_delete_view_success(self):
        response = self.client.delete(reverse('user:user-delete', args=[self.user_to_be_deleted.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_delete_view_failure(self):
        """Test delete inexistent user"""
        response = self.client.delete(reverse('user:user-delete', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_delete_view_failure_unauthenticated(self):
        client = APIClient()
        payload = {'email': 'aaaaaa@test.com','password': 'pass@123',}
        user = create_user(**payload)
        response = client.delete(reverse('user:user-delete', args=[user.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)