from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from .models import Recipe, Tag
from users.models import CustomUser


class CustomRecipeValidator:
    requires_context = True

    def __call__(self, data, author):
        if Recipe.objects.filter(author=author).exists():
            return ValidationError('Такой объект уже существует')

        ingredients = data.get('ingredients')
        set_ingredients = set()
        if not ingredients:
            return ValidationError(
                'Нужно добавить хотя бы один ингредиент.'
            )
        else:
            for ingredient in ingredients:
                if int(ingredient.get('amount')) <= 0:
                    raise ValidationError(
                        ('Значение количества не может быть меньше единицы.')
                    )
                ingredient_id = ingredient.get('id')
                if ingredient_id in set_ingredients:
                    raise ValidationError(
                        'Ингрединеты не должны повторяться'
                    )
                set_ingredients.add(ingredient_id)
        data['ingredients'] = ingredients

        tags = data.get('tags')
        if not tags:
            raise ValidationError(
                'Нужно добавить хотя бы один тэг.'
            )
        elif tags:
            if Tag.objects.filter(id__in=tags).count() < len(tags):
                return ValidationError(
                    'Такого тэга нет в базе.'
                )
        data['tags'] = tags

        cooking_time = data.get('cooking_time')
        if int(cooking_time) < 1:
            return ValidationError(
                'Время приготовления должно быть больше нуля.'
            )
        data['cooking_time'] = cooking_time
        return data


class ValidatorAuthorRecipe:
    '''Валидация доступа к редактироваю.'''
    requires_context = True

    def __call__(self, data, author):
        user_data = dict(data)
        email = user_data.get('email')
        user = get_object_or_404(
            CustomUser,
            email=email,
        )
        if author != user:
            raise ValidationError(
                'Для того, чтобы изменить рецепт,',
                'нужно быть его автором'
            )
        return data
