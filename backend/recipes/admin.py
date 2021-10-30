from django.contrib import admin
from .models import (
    Follow,
    Recipes,
    Tag,
    ShoppingCart,
    Favoritesource,
    Ingredient,
    IngredAmount
)

admin.site.register(Follow)
admin.site.register(Recipes)
admin.site.register(Tag)
admin.site.register(Favoritesource)
admin.site.register(ShoppingCart)
admin.site.register(Ingredient)
admin.site.register(IngredAmount)
