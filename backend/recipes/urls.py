from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    index_api,
    RecipesViewSet,
    UserViewSet,
    IngredientsViewSet,
    TagsViewSet,
    AuthTokenViewSet,
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
v1_router.register('users/', UserViewSet, basename='users')
v1_router.register('users/<int: user_id>', UserViewSet, basename='users_id')
v1_router.register('users/me', UserViewSet, basename='me')
v1_router.register(
    'users/subscriptions',
    UserViewSet,
    basename='subscriptions'
)
v1_router.register('users/suscribe', UserViewSet, basename='suscribe')
v1_router.register('users/set_password', UserViewSet, basename='set_password')
v1_router.register(
    'auth/token/login/',
    AuthTokenViewSet,
    basename='token_login'
)
v1_router.register(
    'auth/token/logout',
    AuthTokenViewSet,
    basename='token_logout'
)


urlpatterns = [
    path('', index_api, name='index'),
    path('v1/', include(v1_router.urls)),
]
