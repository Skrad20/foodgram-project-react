from rest_framework import serializers
from .models import CustomUser, Follow


class UserSerializer(serializers.ModelSerializer):
    '''Сериализация данных по пользователям.'''

    class Meta:
        model = CustomUser
        fields = '__all__'


class PasswordSerializer(serializers.ModelSerializer):
    '''Сериализация для замены пароля.'''
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


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
