# users_app/urls.py
from django.urls import path
from .views import UserListAPI

urlpatterns = [
    path('users/', UserListAPI.as_view(), name="user-list"),                        # GET all + POST
    path('users/<str:uid>/', UserListAPI.as_view(), name="user-detail"),            # GET by ID
]
