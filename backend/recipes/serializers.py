from rest_framework import serializers
from .models import (
    Follow,
    User,
    Recipes,
    Tag,
    ShoppingCart,
    Favoritesource,
    Ingredient
)


class UserSerializer(serializers.ModelSerializer):
    '''Сериализация данных по пользователям.'''

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'firstname',
            'last_name',
            'is_subscriebe',
        ]


class ReciplesSerializer(serializers.ModelSerializer):
    '''Серялизатор данных по рецептам.'''

    class Meta:
        model = Recipes
        fields = [
            'id',
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]


class TagSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по Тэгам.'''

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'slug',
        ]


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по Ингридиентам.'''

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
        ]


class FollowSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по подпискам.'''

    class Meta:
        model = Follow
        fields = [
            'id',
            'user',
            'author',
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по корзине.'''

    class Meta:
        model = ShoppingCart
        fields = [
            'id',
            'user',
            'recipes',
        ]


class FavoritesourceSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по избранному.'''

    class Meta:
        model = Favoritesource
        fields = [
            'id',
            'user',
            'recipe',
        ]
