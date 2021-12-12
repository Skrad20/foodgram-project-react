from django.core.exceptions import ValidationError

from .models import Tag


class CustomRecipeValidator:
    requires_context = True

    def __call__(self, data):
        ingredients = data.get('ingredients')
        set_ingredients = set()
        if not ingredients:
            return ValidationError(
                'Нужно добавить хотя бы один ингредиент.'
            )
        else:
            for ingredient in ingredients:
                if int(ingredient.get('amount')) <= 0:
                    return ValidationError(
                        ('Значение количества не может быть меньше единицы.')
                    )
                ingredient_id = ingredient.get('id')
                if ingredient_id in set_ingredients:
                    return ValidationError(
                        'Ингрединеты не должны повторяться'
                    )
                set_ingredients.add(ingredient_id)
        data['ingredients'] = ingredients

        tags = data.get('tags')
        if not tags:
            return ValidationError(
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

    def __call__(self, data, author, user):
        if user != author:
            raise ValidationError(
                'Для того, чтобы изменить рецепт, нужно быть его автором'
            )
        return data
