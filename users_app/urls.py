from django.urls import path
from .views import (
    UserListAPI,
    UserDetailAPI,
    UserCreateAPI,
    UserUpdateAPI,
    UserDeleteAPI
)

urlpatterns = [
    path('user/create/', UserCreateAPI.as_view(), name='user-create-api'),              # POST - Create User
    path('user/', UserListAPI.as_view(), name='user-list-api'),                        # GET all users
    path('user/<str:uid>/', UserDetailAPI.as_view(), name='user-detail-api'),          # GET single user
    path('user/update/<str:uid>/', UserUpdateAPI.as_view(), name='user-update-api'),    # PUT - Update User
    path('user/delete/<str:uid>/', UserDeleteAPI.as_view(), name='user-delete-api'),    # DELETE - Delete User
]
