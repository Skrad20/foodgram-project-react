from django.contrib import admin
from .models import (
    Recipe,
    Tag,
    ShoppingCart,
    Favoritesource,
    Ingredient,
    IngredAmount
)


admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Favoritesource)
admin.site.register(ShoppingCart)
admin.site.register(Ingredient)
admin.site.register(IngredAmount)


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ['tag', 'name']


class TagtAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_EN', 'color', 'slug', 'colored_name')
    list_filter = ["name"]
