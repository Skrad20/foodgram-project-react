from rest_framework import serializers
from .models import (
    Recipe,
    Tag,
    ShoppingCart,
    Favoritesource,
    Ingredient,
    IngredAmount
)
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    '''Сериализация данных по пользователям.'''

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'id',
            'username',
            'firstname',
            'last_name',
            'is_subscriebe',
        ]


class TagSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по Тэгам.'''

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по Ингридиентам.'''

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredAmountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()
    amount = serializers.StringRelatedField()

    class Meta:
        model = IngredAmount
        fields = ('id', 'name', 'amount', 'measurement_unit')


class ReciplesSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по рецептам.'''
    ingredients = IngredAmountSerializer(
        many=True,
        read_only=True,
    )
    author = serializers.StringRelatedField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
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
            'ingredients',
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по корзине.'''

    class Meta:
        model = ShoppingCart
        fields = [
            'id',
            'user',
            'recipe',
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
