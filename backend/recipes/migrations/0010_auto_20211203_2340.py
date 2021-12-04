# Generated by Django 3.2 on 2021-12-03 20:40

from django.db import migrations, models
import recipes.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='Теги связанные с рецептами'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=recipes.fields.ColorField(choices=[('#0000FF', 'Синий'), ('#FFA500', 'Оранжевый'), ('#008000', 'Зеленый'), ('#800080', 'Фиолетовый'), ('#FFFF00', 'Желтый'), ('#000000', 'Чёрный'), ('#ff0000', 'Красный'), ('#42aaff', 'Голубой')], default='#008000', max_length=7, verbose_name='Цвет HEX'),
        ),
    ]