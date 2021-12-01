from django.contrib import admin
from .models import (
    Recipe,
    Tag,
    ShoppingCart,
    Favoritesource,
    Ingredient,
    IngredAmount
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    list_filter = ['name', 'author', 'tags']


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_filter = ['name']


class TagAdmin(admin.ModelAdmin):
    list_filter = ['name', 'slug']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favoritesource)
admin.site.register(ShoppingCart)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredAmount)


