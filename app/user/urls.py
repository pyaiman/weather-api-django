"""
URL mappings for the user API.
"""
from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailsView.as_view(), name='user-details'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
