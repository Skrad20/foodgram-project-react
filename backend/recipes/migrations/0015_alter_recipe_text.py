# Generated by Django 3.2 on 2021-12-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_alter_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(max_length=5000, verbose_name='Текст рецепта'),
        ),
    ]