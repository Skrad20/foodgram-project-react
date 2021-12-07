from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response

from .filters import FilterRecipe, IngredientFilter
from .models import (Favorite, IngredAmount, Ingredient, Recipe, ShoppingCart,
                     Tag)
from .pagination import CustomPagination, PageNumberPaginationDataOnly
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)


class RecipesViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по рецептам.
    Отвечает по адресам:
    'recipes/'
    'recipes/id/'
    'recipes/id/favorite/'
    'recipes/id/shopping_cart/'
    '''
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]
    filterset_class = FilterRecipe
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, )
    pagination_class = CustomPagination
    filterset_fields = (
        'is_favorited',
        'is_in_shopping_cart',
        'author',
        'tags',
    )
    search_fields = ('name', 'text', 'ingredients__name')
    ordering_fields = ('name', 'pub_date')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        methods=['GET', ],
        name='Скачивание карты покупок',
    )
    def favorite(self, request, pk=None):
        '''
        Реализует добавление в избранное рецепта.
        Доступно только авторизованным пользователям.
        '''
        recipe = get_object_or_404(Recipe, id=pk)
        if Favorite.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            data = {
                'errors': 'Рецепт уже добавлен в избранное.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        favorite_cart = Favorite.objects.create(
            user=request.user,
            recipe=recipe
        )
        favorite_cart.save()
        serializer = FavoriteSerializer(recipe)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        '''
        Реализует удаление рецепта из избранного.
        Доступно только авторизованным пользователям.
        '''
        recipe = get_object_or_404(Recipe, id=pk)
        if not Favorite.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            data = {
                'errors': 'Этого рецепта нет в избранном.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        favorite_cart = get_object_or_404(
            Favorite,
            user=request.user,
            recipe=recipe
        )
        favorite_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['GET', ],
        permission_classes=[IsAuthenticated],
        name='Скачивание карты покупок',
    )
    def shopping_cart(self, request, pk=None):
        '''
        Добавление рецепта в список покупок.
        Доступно только авторизованным пользователям.
        '''
        recipe = get_object_or_404(Recipe, id=pk)
        if ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            data = {
                'errors': 'Рецепт уже в списке покупок.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        shop_cart = ShoppingCart.objects.create(
            user=request.user,
            recipe=recipe
        )
        shop_cart.save()
        serializer = ShoppingCartSerializer(
            shop_cart,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        '''
        Реализует удаление рецепта из избранного.
        Доступно только авторизованным пользователям.
        '''
        recipe = get_object_or_404(Recipe, id=pk)
        if not ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            data = {
                'errors': 'Этого рецепта нет в списке покупок.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        shop_cart = get_object_or_404(
            ShoppingCart,
            user=request.user,
            recipe=recipe
        )
        shop_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET', ],
        permission_classes=[IsAuthenticated],
        name='Скачивание карты покупок',
    )
    def download_shopping_cart(self, request, pk=None):
        '''
        Реализует сохранение списка покупок.
        Доступно только авторизованным пользователям.
        '''
        shop_cart = IngredAmount.objects.filter(
            recipe__cart__user=request.user).values_list(
                'ingredient__name',
                'amount',
                'ingredient__measurement_unit',
        )
        shop_list = {}
        for item in shop_cart:
            name = item[0]
            if name in shop_list:
                shop_list[name]['amount'] += item[1]
            else:
                shop_list[name] = {
                    'amount': item[1],
                    'measurement_unit': item[2],
                }

        data = ['Список ингредиентов\n', ]
        for key in shop_list.keys():
            amount_res = (shop_list[key]['amount'])
            unit = (shop_list[key]['measurement_unit'])
            data.append(f'{key}: {amount_res} {unit}\n')
        date = timezone.now()
        response = HttpResponse(data, 'Content-Type: text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename="shoplist_{date}.txt"'
        )
        return response


class TagsViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по тэгам.
    Отвечает по адресам:
    'tags/'
    'tags/id/'
    '''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPaginationDataOnly


class IngredientsViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по ингедиентам.
    Отвечает по адресам:
    'ingredients/'
    'ingredients/id/'
    '''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = IngredientFilter
    pagination_class = PageNumberPaginationDataOnly
    search_fields = ('^name',)
    ordering_fields = ('name',)


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
    permission_classes = [IsAuthenticated]


class FavoriteViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по списку избранного.
    Отвечает по адресам:
    'recipes/id/favorite/'
    '''
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    permission_classes = [IsAuthenticated]
