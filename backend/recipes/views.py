from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView, Response
from rest_framework import (
    permissions,
    serializers,
    viewsets,
    filters,
    mixins,
)

from .serializers import (
    FavoritesourceSerializer,
    IngredientSerializer,
    ShoppingCartSerializer,
    TagSerializer,
    UserSerializer,
    ReciplesSerializer,

)

from .models import (
    User,
    Recipes,
    Tag,
    ShoppingCart,
    Favoritesource,
    Ingredient
)



def index_api(request):
    return HttpResponse('Онсновная страница API')


class index_recipes(viewsets.ModelViewSet):
    def get(self, request, format=None):
        return HttpResponse('Онсновная страница API')


class UserViewSet(viewsets.ModelViewSet):
    '''Возвращает данные по пользователям.'''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    '''Возвращает данные по рецептам.'''
    queryset = Recipes.objects.all()
    serializer_class = ReciplesSerializer


class TagsViewSet(viewsets.ModelViewSet):
    '''Возвращает данные по тэгам'''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    '''Возвращает данные по ингедиентам.'''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class ShoppingCartViewSer(viewsets.ModelViewSet):
    '''Возвращает данные по корзине.'''
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    '''Возвращает данные по избранному.'''
    queryset = Favoritesource.objects.all()
    serializer_class = FavoritesourceSerializer


class AuthTokenViewSet(viewsets.ModelViewSet):
    '''Возвращает данные по токенам.'''
    queryset = Recipes.objects.all()
    serializer_class = ReciplesSerializer
