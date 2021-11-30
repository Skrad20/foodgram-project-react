from django.db import models
from django.core import validators
from django.contrib import admin
from django.utils.html import format_html
from .config import COLOR_CHOICES
from .fields import ColorField
from users.models import (
    CustomUser,
)


class Tag(models.Model):
    '''Данные по тэгам.'''
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        unique=True,
    )
    color = ColorField(
        max_length=20,
        verbose_name='Цвет',
        default='008000',
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Адрес',
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'Tags'
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['id']

    @admin.display
    def colored_name(self):
        return format_html(
            '<span style="color: #{};;width=10px;height=10px;""></span>',
            self.hexcolor,
        )


class TagtAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_EN', 'color', 'slug', 'colored_name')


class Ingredient(models.Model):
    '''Данные по ингредиентам.'''
    name = models.CharField(
        max_length=50,
        verbose_name='Название продукта',
        unique=True,
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
    )

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'Ingredients'
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['-id']


class Recipe(models.Model):
    '''Данные по рецептам.'''
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги свяpанные с рецептами',
        related_name='recipes',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes',
    )
    is_favorited = models.BooleanField(
        verbose_name='Проверка на наличие в избранном',
        blank=True,
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='Проверка на наличие в карте покупок',
        blank=True,
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=500,
    )
    image = models.ImageField(
        blank=True
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Текст рецепта',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=[validators.MinValueValidator(1)]
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredAmount',
        verbose_name='Ингридиенты',
        related_name='recipes',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'
        db_table = 'Recipes'
        ordering = ['-id']


class IngredAmount(models.Model):
    '''Связь кол-ва ингредиента и рецепта'''
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='ingredients_amounts',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredients_amounts',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
        validators=[
            validators.MinValueValidator(
                0,
                message='Количество не может быть ниже нуля'
            )
        ]
    )

    def __str__(self):
        return self.ingredient.name

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        db_table = 'IngredAmount'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='recipe_ingredient_unique',
            )
        ]


class ShoppingCart(models.Model):
    '''Список покупок.'''
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        related_name='cart',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты',
        related_name='cart',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user.username} купит {self.recipe.name}'

    class Meta:
        db_table = 'ShoppingCarts'
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ['-id']


class Favoritesource(models.Model):
    '''Избранное.'''
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        verbose_name='Рецепты',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user}: {self.recipe}'

    class Meta:
        db_table = 'Favoritesource'
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списоки избранного'
        ordering = ['-id']
