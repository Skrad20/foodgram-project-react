from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (Favorite, IngredAmount, Ingredient, Recipe, ShoppingCart,
                     Tag)
from .validators import CustomRecipeValidator, ValidatorAuthorRecipe
from users.serializers import UserSerializer


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
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField()
    amount = serializers.StringRelatedField()

    class Meta:
        model = IngredAmount
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по рецептам.'''

    author = UserSerializer(read_only=True)
    ingredients = IngredAmountSerializer(
        source='ingredients_amounts',
        many=True,
        #read_only=True,
        partial=True
    )
    tags = TagSerializer(
        many=True,
        read_only=True,
        partial=True
    )
    image = Base64ImageField(read_only=True)
    cooking_time = serializers.IntegerField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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

        read_only_fields = ['id', 'author']
        depth = 1

    def validate(self, data: dict) -> dict:
        '''
        Валидация данных сериалаизатора.
        '''
        data = self.initial_data
        recipe_id = self.context['view'].kwargs.get('pk')
        recipe = Recipe.objects.filter(id=recipe_id)[0]
        author = recipe.author
        data = CustomRecipeValidator().__call__(
            data,
        )
        request = self.context.get('request')
        if request.method == 'PATCH':
            user = request.user
            data = ValidatorAuthorRecipe().__call__(
                data, author, user,
            )
        return data

    def create(self, data):
        '''
        Обновленный метод создания рецептов.
        '''
        tags = data.pop('tags')
        ingredients = data.pop('ingredients')
        if data.get('image') is not None:
            image = data.pop('image')
            recipe = Recipe.objects.create(image=image, **data)
        recipe = Recipe.objects.create(**data)
        self.add_tags_to_recipe(tags, recipe)
        self.update_ingredients_in_recipe(ingredients, recipe)
        return recipe

    def update(self, recipe: Recipe, data):
        '''
        Обновленный метод обновления рецептов.
        '''
        recipe.name = data.get('name', recipe.name)
        recipe.text = data.get('text', recipe.text)
        recipe.cooking_time = data.get(
            'cooking_time',
            recipe.cooking_time
        )
        recipe.image = data.get('image', recipe.image)
        if 'ingredients' in data:
            ingredients = data.pop('ingredients')
            recipe.ingredients.clear()
            self.update_ingredients_in_recipe(ingredients, recipe)
        if 'tags' in data:
            tags_data = data.pop('tags')
            recipe.tags.set(tags_data)
        recipe.save()
        return recipe

    @staticmethod
    def add_tags_to_recipe(tags, recipe):
        '''Добавляет данные по тэгам.'''
        for tag_id in tags:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))

    @staticmethod
    def update_ingredients_in_recipe(ingredients, recipe):
        '''Добавляет данные по рецептам'''
        for ingredient in ingredients:
            IngredAmount.objects.create(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient,
                    pk=ingredient.get('id')
                ),
                amount=ingredient.get('amount')
            )

    def get_is_favorited(self, obj):
        '''
        Проверяет наличие рецепта в списке избранного.
        '''
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        '''
        Проверяет наличие рецепта в списке покупок.
        '''
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredAmount
        fields = ('id', 'amount')


class ShoppingCartSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по корзине.'''

    class Meta:
        model = ShoppingCart
        fields = [
            'id',
            'user',
            'recipe',
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по рецептам в избранное.'''
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]
