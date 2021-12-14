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
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.FloatField()

    class Meta:
        model = IngredAmount
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор данных по рецептам.'''

    author = UserSerializer(read_only=True)
    ingredients = IngredAmountSerializer(
        source='ingredients_amounts',
        many=True
    )
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    image = Base64ImageField(max_length=None, use_url=True)
    cooking_time = serializers.FloatField()
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
        ingredients_data = data.pop('ingredients_amounts')
        list_res_in_data = []
        for item in ingredients_data:
            data_item = list(item.values())
            dict_ingredients = {}
            dict_ingredients['id'] = data_item[0]['id']
            dict_ingredients['amount'] = data_item[1]
            list_res_in_data.append(dict_ingredients)
        data['ingredients'] = list_res_in_data
        data['tags'] = self.initial_data['tags']
        CustomRecipeValidator().__call__(
            data,
        )
        request = self.context.get('request')
        if request.method == 'PATCH' or request.method == 'DELETE':
            recipe_id = self.context['view'].kwargs.get('pk')
            recipe = Recipe.objects.filter(id=recipe_id)[0]
            author = recipe.author
            user = request.user
            ValidatorAuthorRecipe().__call__(
                data, author, user,
            )
        return data

    def create(self, data):
        '''
        Обновленный метод создания рецептов.
        '''
        tags = data.pop('tags')
        ingredients = data.pop('ingredients')
        image = data.pop('image')
        recipe = Recipe.objects.create(image=image, **data)
        self.add_tags_to_recipe(tags, recipe)
        self.update_ingredients_in_recipe(ingredients, recipe)
        return recipe

    def update(self, recipe: Recipe, data):
        '''
        Обновленный метод обновления рецептов.
        '''
        ingredients = data.pop('ingredients')
        tags_data = data.pop('tags')
        ret = super().update(recipe, data)
        if ingredients:
            ret.ingredients.clear()
            self.update_ingredients_in_recipe(ingredients, ret)
        if tags_data:
            ret.tags.set(tags_data)
        ret.save()
        return ret

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
