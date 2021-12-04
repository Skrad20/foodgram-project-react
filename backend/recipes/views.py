from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import Response
from rest_framework import (
    viewsets,
    status,
)
from rest_framework.permissions import AllowAny
from django.shortcuts import (
    get_object_or_404,
)
from .pagination import (
    CustomPagination,
    PageNumberPaginationDataOnly
)
from .serializers import (
    FavoritesourceSerializer,
    IngredientSerializer,
    ShoppingCartSerializer,
    TagSerializer,
    RecipeSerializer,
    CreateRecipeSerializer
)
from .filters import (
    FilterRecipe,
    IngredientFilter,
)
from users.models import CustomUser
from .models import (
    Recipe,
    IngredAmount,
    Tag,
    ShoppingCart,
    Favoritesource,
    Ingredient,
)
import datetime


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        methods=['get', ],
        name='Скачивание карты покупок',
    )
    def favorite(self, request, pk=None):
        '''
        Реализует добавление в избранное рецепта.
        Доступно только авторизованным пользователям.
        '''
        user = get_object_or_404(CustomUser, email=request.user)
        recipe = get_object_or_404(Recipe, id=pk)
        print(self.request.query_params)
        if Favoritesource.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            data = {
                'errors': 'Рецепт уже добавлен в избранное.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        favorite_cart = Favoritesource.objects.create(user=user, recipe=recipe)
        favorite_cart.save()
        (Favoritesource.objects.filter(user=user))
        serializer = FavoritesourceSerializer(recipe)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        '''
        Реализует удаление рецепта из избранного.
        Доступно только авторизованным пользователям.
        '''
        user = get_object_or_404(CustomUser, email=request.user)
        recipe = get_object_or_404(Recipe, id=pk)
        if not Favoritesource.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            data = {
                'errors': 'Этого рецепта нет в избранном.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        favorite_cart = get_object_or_404(
            Favoritesource,
            user=user,
            recipe=recipe
        )
        favorite_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['get', ],
        permission_classes=[IsAuthenticated],
        name='Скачивание карты покупок',
    )
    def shopping_cart(self, request, pk=None):
        '''
        Добавление рецепта в список покупок.
        Доступно только авторизованным пользователям.
        '''
        user = get_object_or_404(CustomUser, email=request.user)
        recipe = get_object_or_404(Recipe, id=pk)
        if ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            data = {
                'errors': 'Рецепт уже в списке покупок.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        shop_cart = ShoppingCart.objects.create(user=user, recipe=recipe)
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
        user = get_object_or_404(CustomUser, email=request.user)
        recipe = get_object_or_404(Recipe, id=pk)
        if not ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            data = {
                'errors': 'Этого рецепта нет в списке покупок.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        shop_cart = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
        shop_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get', ],
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
        date = datetime.datetime.now()
        filename = f'Список покупок {date}.csv'
        response = HttpResponse(content_type='text/csv')
        response["Content-Disposition"] = f"attachment; filename={filename}"
        template = loader.get_template('upload_template.txt')

        data = ['Список ингредиентов', ]
        for key in shop_list.keys():
            amount_res = shop_list[key]['amount']
            unit = shop_list[key]['measurement_unit']
            data.append(f'{key}: {amount_res} {unit}')
        resuolt = {'data': data}
        response.write(template.render(resuolt).encode("utf-8"))
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


class FavoriteViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по списку избранного.
    Отвечает по адресам:
    'recipes/id/favorite/'
    '''
    queryset = Favoritesource.objects.all()
    serializer_class = FavoritesourceSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
