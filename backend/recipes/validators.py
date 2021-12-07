from django.core.exceptions import ValidationError

from .models import Recipe


class CustomRecipeValidator:
    requires_context = True

    def __call__(self, data, author, is_recipe, serializer):
        if Recipe.objects.filter(author=author).exists() and is_recipe:
            return ValidationError('Такой объект уже существует')
        return data
