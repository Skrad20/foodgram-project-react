from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from .models import (
    CustomUser,
    Follow
)


class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserSerializer(serializers.ModelSerializer):
    '''Сериализация данных по пользователям.'''
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if (request is None or request.user.is_anonymous):
            return False
        return Follow.objects.filter(
            user=request.user, author=obj.id
        ).exists()


class PasswordSerializer(serializers.ModelSerializer):
    '''Сериализация для замены пароля.'''
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            'new_password',
            'current_password',
        ]


class FollowSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по подпискам.'''
    user = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Follow
        fields = [
            'id',
            'user',
            'author',
        ]
