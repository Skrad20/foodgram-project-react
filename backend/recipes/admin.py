from django.contrib import admin
from .models import (
    Follow,
    Recipe,
    Tag,
    ShoppingCart,
    Favoritesource,
    Ingredient,
    IngredAmount
)

admin.site.register(Follow)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Favoritesource)
admin.site.register(ShoppingCart)
admin.site.register(Ingredient)
admin.site.register(IngredAmount)
