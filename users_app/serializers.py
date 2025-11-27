# users_app/serializers.py

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'uid', 'email', 'name', 'mobile_no', 'state', 'district',
            'city_village', 'pin_code', 'photo_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


