from rest_framework import serializers
from .models import User

class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'confirm_password', 'aadhar', 'address']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password and Confirm Password do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')                          # remove confirm_password
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
