from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    '''Данные по тэгам.'''
    BLUE = '#0000FF'
    ORANGE = '#FFA500'
    GREEN = '#008000'
    PURPLE = '#800080'
    YELLOW = '#FFFF00'

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый'),
    ]

    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        unique=True,
    )
    color = models.CharField(
        max_length=20,
        verbose_name='Цвет',
        choices=COLOR_CHOICES,
        blank=True,
        null=True,
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
        ordering = ['-id']


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


class Recipes(models.Model):
    '''Данные по рецептам.'''
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги свяpанные с рецептами',
        related_name='recipes',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes',
    )
    is_favorited = models.BooleanField(
        verbose_name='Проверка на наличие в избранном',
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='Проверка на наличие в карте покупок',
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
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredAmount',
        verbose_name='Ингридиенты',
        related_name='recipes',
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
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    amout = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
        validators=[
            validators.MinValueValidator(
                1,
                message='Количество не может быть ниже единицы'
            )
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        db_table = 'IngredAmount'
        ordering = ['-id']


class Follow(models.Model):
    ''''Описывает работу подписок.'''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'Following'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']


class ShoppingCart(models.Model):
    '''Список покупок.'''
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='cart',
        on_delete=models.CASCADE
    )
    recipes = models.ForeignKey(
        Recipes,
        verbose_name='Рецепты',
        related_name='cart',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'ShoppingCarts'
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ['-id']


class Favoritesource(models.Model):
    '''Избранное.'''
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='favorites',
        verbose_name='Рецепты',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'Favoritesource'
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списоки избранного'
        ordering = ['-id']
