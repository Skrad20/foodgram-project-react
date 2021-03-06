from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.pagination import CustomPagination
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, Follow
from .serializers import (AuthTokenSerializer, CustomUserCreateSerializer,
                          FollowSerializer, FollowSerializerView,
                          PasswordSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по пользователям.
    Отвечает по адресам:
    'users/'
    'users/id/'
    'users/me/'
    'users/set_password/'
    '''
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, )
    pagination_class = CustomPagination
    permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return CustomUserCreateSerializer

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=[IsAuthenticated, ],
        name='Изменение пароля',
    )
    def set_password(self, request, pk=None):
        '''
        Реализует механизм смены пароля.
        Только POST запросы и только авторизованные.
        '''
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False,
        methods=['GET', ],
        permission_classes=[IsAuthenticated],
        name='Личная страница пользователя',
    )
    def me(self, request, pk=None):
        '''
        Личная страница пользователя.
        Только авторизованные.
        '''
        queryset = CustomUser.objects.filter(email=request.user)
        serializer = UserSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data[0], status=status.HTTP_200_OK)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        name='Подписки на пользователей',
    )
    def subscriptions(self, request, id=None):
        '''
        Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        '''
        queryset = Follow.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializerView(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        name='Подписаться на пользователя',
    )
    def subscribe(self, request, pk):
        '''
        Осуществляет подписку на пользователя.
        '''
        author = get_object_or_404(CustomUser, id=pk)
        if author == request.user:
            data = {
                'errors': 'Нельзя подписаться на самого себя.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(
            user=request.user,
            author=author.id
        ).exists():
            data = {
                'errors': 'Подписка уже существует'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(user=request.user, author=author)
        follow.save()

        serializer = FollowSerializer(
            follow,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, pk):
        '''
        Осуществляет отписку от пользователя.
        '''
        author = get_object_or_404(CustomUser, id=pk)
        if not Follow.objects.filter(
            user=request.user,
            author=author.id
        ).exists():
            data = {
                'errors': 'Такой подписки не существует.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        subscription = get_object_or_404(
            Follow,
            user=request.user,
            author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'auth_token': str(token)},
            status=status.HTTP_200_OK
        )


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
