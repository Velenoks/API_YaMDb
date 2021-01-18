from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
        model = User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
        )
        model = User


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'email',
            'confirmation_code'
        )
        model = User
