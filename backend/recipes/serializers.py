from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import (Favorite, IngredAmount, Ingredient, Recipe, ShoppingCart,
                     Tag)


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
        source="ingredients_amounts",
        many=True,
        read_only=True,
    )
    tags = TagSerializer(many=True, read_only=True)
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

    def ingredients_unique(self, ingredients):
        '''
        Приводит данные по ингредиентам к формату.
        id - количество.
        Убирает повторы, суммируя вес.
        '''
        dict_ingred = {}
        for item in ingredients:
            id = item.get('id')
            amount = item.get('amount')
            if id in dict_ingred.keys():
                dict_ingred[id] += amount
            else:
                dict_ingred[id] = amount
        ingredients_list = []
        for i in range(len(dict_ingred.keys())):
            key = list(dict_ingred.keys())[i]
            ingredients_list.append(
                {
                    'id': key,
                    'amount': dict_ingred[key],
                }
            )
        return ingredients_list

    def validate(self, data: dict) -> dict:
        '''
        Валидация данных сериалаизатора.
        '''
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = self.ingredients_unique(ingredients)
        if not ingredients_list:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы один ингредиент.'
            )
        else:
            for ingredient in ingredients_list:
                if int(ingredient.get('amount')) <= 0:
                    raise serializers.ValidationError(
                        ('Значение количества не может быть меньше единицы.')
                    )
                ingredient_id = ingredient.get('id')
                if ingredient_id in ingredients_list:
                    raise serializers.ValidationError(
                        'Ингрединеты не должны повторяться'
                    )
        data['ingredients'] = ingredients_list

        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы один тэг.'
            )
        elif tags:
            if Tag.objects.filter(id__in=tags).count() < len(tags):
                raise serializers.ValidationError(
                    'Такого тэга нет в базе.'
                )
        data['tags'] = tags

        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) < 1:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше нуля.'
            )
        data['cooking_time'] = cooking_time
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
        recipe.name = data.get(
            'name',
            recipe.name
        )
        recipe.text = data.get(
            'text',
            recipe.text
        )
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
