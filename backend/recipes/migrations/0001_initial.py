# Generated by Django 3.2 on 2021-11-05 18:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favoritesource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Список избранного',
                'verbose_name_plural': 'Списоки избранного',
                'db_table': 'Favoritesource',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='IngredAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0, message='Количество не может быть ниже нуля')], verbose_name='Количество ингредиента')),
            ],
            options={
                'verbose_name': 'Количество ингредиента',
                'verbose_name_plural': 'Количество ингредиентов',
                'db_table': 'IngredAmount',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название продукта')),
                ('measurement_unit', models.CharField(max_length=20, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'db_table': 'Ingredients',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favorited', models.BooleanField(blank=True, default=False, verbose_name='Проверка на наличие в избранном')),
                ('is_in_shopping_cart', models.BooleanField(blank=True, default=False, verbose_name='Проверка на наличие в карте покупок')),
                ('name', models.CharField(max_length=500, verbose_name='Название рецепта')),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('text', models.TextField(max_length=500, verbose_name='Текст рецепта')),
                ('cooking_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Рецепты',
                'verbose_name_plural': 'Рецепты',
                'db_table': 'Recipes',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('color', models.CharField(blank=True, choices=[('#0000FF', 'Синий'), ('#FFA500', 'Оранжевый'), ('#008000', 'Зеленый'), ('#800080', 'Фиолетовый'), ('#FFFF00', 'Желтый')], max_length=20, null=True, verbose_name='Цвет')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'db_table': 'Tags',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='recipes.recipe', verbose_name='Рецепты')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
                'db_table': 'ShoppingCarts',
                'ordering': ['-id'],
            },
        ),
    ]
