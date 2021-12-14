# Generated by Django 3.2 on 2021-12-14 07:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredamount',
            name='amount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0, message='Количество не может быть ниже нуля')], verbose_name='Количество ингредиента'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления'),
        ),
    ]
