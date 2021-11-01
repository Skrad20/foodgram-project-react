from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView, Response
from rest_framework import (
    permissions,
    serializers,
    viewsets,
    filters,
    mixins,
    status,
)

from .serializers import (
    FavoritesourceSerializer,
    IngredientSerializer,
    ShoppingCartSerializer,
    TagSerializer,
    ReciplesSerializer,

)
from users.models import CustomUser
from .models import (
    Recipe,
    Tag,
    ShoppingCart,
    Favoritesource,
    Ingredient,
)


class RecipesViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по рецептам.
    Отвечает по адресам:
    'recipes/'
    'recipes/id/'
    'recipes/id/favorite/'
    'recipes/id/shopping_cart/'
    '''
    queryset = Recipe.objects.all()
    serializer_class = ReciplesSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]


class TagsViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по тэгам.
    Отвечает по адресам:
    'tags/'
    'tags/id/'
    '''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]


class IngredientsViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по ингедиентам.
    Отвечает по адресам:
    'ingredients/'
    'ingredients/id/'
    '''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]


class ShoppingCartViewSer(viewsets.ModelViewSet):
    '''
    Возвращает данные по корзине.
    Отвечает по адресам:
    'recipes/download_shopping_cart/'
    'recipes/id/download_shopping_cart/'
    '''
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request, pk=None):
        '''
        Реализует сохранение списка покупок.
        Доступно только авторизованным пользователям.
        '''
        pass


class FavoriteViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по списку избранного.
    Отвечает по адресам:
    'recipes/id/favorite/'
    '''
    queryset = Favoritesource.objects.all()
    serializer_class = FavoritesourceSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
