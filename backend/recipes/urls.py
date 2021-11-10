from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RecipesViewSet,
    IngredientsViewSet,
    TagsViewSet,
)


v1_router = DefaultRouter()
v1_router.register('recipes', RecipesViewSet, basename='recipes')
v1_router.register(
    'recipes/<int: recipes_id>',
    RecipesViewSet,
    basename='recipes_id'
)
v1_router.register(
    'recipes/download_shopping_cart',
    RecipesViewSet,
    basename='download_shopping_cart'
)
v1_router.register(
    'recipes/<int: recipes_id>/shopping_cart',
    RecipesViewSet,
    basename='shopping_cart'
)
v1_router.register(
    'recipes/<int: recipes_id>/favorite',
    RecipesViewSet,
    basename='recipes_favorite'
)
v1_router.register('tags', TagsViewSet, basename='tags')
v1_router.register('tags/<int: tag_id>', TagsViewSet, basename='tags_id')
v1_router.register('ingredients', IngredientsViewSet, basename='ingredients')
v1_router.register(
    'ingredients/<int: ingredient_id>',
    IngredientsViewSet,
    basename='ingredient_id'
)

urlpatterns = [
    path('', include(v1_router.urls)),
]
