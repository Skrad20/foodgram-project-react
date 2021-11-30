from rest_framework import serializers
from django.contrib.auth import authenticate
from djoser.serializers import UserCreateSerializer
from backend.recipes.models import Recipe
from backend.recipes.serializers import RecipeSerializer

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


class FollowSerializerView(serializers.ModelSerializer):
    '''Сериализатор данных по подпискам.'''

    id = serializers.ReadOnlyField('author.id')
    email = serializers.ReadOnlyField('author.email')
    username = serializers.ReadOnlyField('author.username')
    first_name = serializers.ReadOnlyField('author.first_name')
    last_name = serializers.ReadOnlyField('author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = [
            'id', 'email', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'recipes',
            'recipes_count'
        ]

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = int(request.Get.get('recipes_limit'))
        queryset = Recipe.objects.filter(author=obj.author)
        if recipes_limit:
            queryset = queryset[:recipes_limit]
        return RecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Email')
    password = serializers.CharField(
        label=('Password',),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Неверные учетные данные.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Запрос должен содержать email и пароль.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
