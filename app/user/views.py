"""
Views for the user API
"""
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from user.serializers import UserSerializer, AuthTokenSerializer
from django.contrib.auth import get_user_model


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
    
class UserListView(generics.ListAPIView):
    """List all users in the system."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UserDetailsView(generics.RetrieveAPIView):
    """Retrieve a specific user's details."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    
class UserUpdateView(generics.UpdateAPIView):
    """Update a specific user's details."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    
class UserDeleteView(generics.DestroyAPIView):
    """Delete a specific user."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
