from rest_framework import status
from .models import Recipe


class CustomRecipeValidator:
    requires_context = True

    def __call__(self, data, author, is_recipe, serialisator):
        if Recipe.objects.filter(author=author).exists() and is_recipe:
            print('Есть уже такой')
        return data
