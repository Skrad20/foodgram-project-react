from django_filters import rest_framework as filters
from .models import (
    Recipe,
    CustomUser,
    Ingredient,
)


class IngredientFilter(filters.FilterSet):
    '''Фильтрует ингредиенты по названию'''
    name = filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class FilterRecipe(filters.FilterSet):
    '''Фтльтрует рецепты по нахлждению в карте покупок и в избранном.'''

    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous:
            return queryset
        return queryset.filter(favorites__user=user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous:
            return queryset
        return queryset.filter(cart__user=user)

    class Meta:
        model = Recipe
        fields = [
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        ]
