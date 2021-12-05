from django.contrib import admin
from .models import (
    Recipe,
    Tag,
    ShoppingCart,
    Favoritesource,
    Ingredient,
    IngredAmount
)


class IngredientAmountInLine(admin.TabularInline):
    model = IngredAmount


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'favorited']
    list_filter = ['name', 'author', 'tags']
    search_fields = ['^name', ]
    inlines = [IngredientAmountInLine]

    def favorited(self, obj):
        return Favoritesource.objects.filter(recipe=obj).count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_filter = ['name']
    search_fields = ['^name', 'measurement_unit']


class TagAdmin(admin.ModelAdmin):
    list_filter = ['name', 'slug']
    search_fields = ['^name', '^slug']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favoritesource)
admin.site.register(ShoppingCart)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredAmount)
