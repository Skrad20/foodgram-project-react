from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from .models import Recipe
from users.models import CustomUser


class CustomRecipeValidator:
    requires_context = True

    def __call__(self, data, author, is_recipe, serializer):
        if Recipe.objects.filter(author=author).exists() and is_recipe:
            return ValidationError('Такой объект уже существует')
        return data


class Validator:
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
