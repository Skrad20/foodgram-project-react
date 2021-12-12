from django.core import validators
from django.db import models

from .fields import ColorField
from users.models import CustomUser


class Tag(models.Model):
    '''Данные по тэгам.'''
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        unique=True,
    )
    BLUE = '#0000FF'
    ORANGE = '#FFA500'
    GREEN = '#008000'
    RED = '#ff0000'
    BLACK = '#000000'
    PURPLE = '#800080'
    YELLOW = '#FFFF00'
    LIGHT_BLUE = '#42aaff'
    CHOICES_COLOR = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый'),
        (BLACK, 'Чёрный'),
        (RED, 'Красный'),
        (LIGHT_BLUE, 'Голубой'),
    ]
    color = ColorField(
        max_length=7,
        choices=CHOICES_COLOR,
        verbose_name='Цвет HEX',
        default=LIGHT_BLUE,
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Адрес',
        unique=True,
    )

    class Meta:
        db_table = 'Tags'
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    '''Данные по ингредиентам.'''
    name = models.CharField(
        max_length=100,
        verbose_name='Название продукта',
        unique=True,
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
    )

    class Meta:
        db_table = 'Ingredients'
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    '''Данные по рецептам.'''
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги связанные с рецептами',
        related_name='recipes',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=500,
    )
    image = models.ImageField(
        max_length=500000,
        upload_to='recipes/',
        verbose_name='Картинки',
        blank=True
    )
    text = models.TextField(
        max_length=5000,
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

    class Meta:
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'
        db_table = 'Recipes'
        ordering = ['-id']

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.ingredient.name


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

    class Meta:
        db_table = 'ShoppingCarts'
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Уникальные рецепты в списке покупок'
            )
        ]

    def __str__(self):
        return f'{self.user.username} купит {self.recipe.name}'


class Favorite(models.Model):
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

    class Meta:
        db_table = 'Favoritesource'
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списоки избранного'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Уникальный список рецептов в избранном'
            )
        ]

    def __str__(self):
        return f'{self.user}: {self.recipe}'
