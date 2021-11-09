from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from rest_framework.authentication import TokenAuthentication
from rest_framework import (
    pagination,
    permissions,
    serializers,
    viewsets,
    filters,
    mixins,
    status,
)
from .serializers import (
    UserSerializer,
    CustomUserCreateSerializer,
    FollowSerializer,
    PasswordSerializer,
)
from .models import (
    Follow,
    CustomUser,
)


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
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = CustomUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated, ],
        name='Изменение пароля',
    )
    def set_password(self, request, pk=None):
        '''
        Реализует механизм смены пароля.
        Только POST запросы и только авторизованные.
        '''
        user = get_object_or_404(CustomUser, email=request.user)
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                serializer.data,
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        methods=['get', ],
        permission_classes=[IsAuthenticated, ],
        name='Личная страница пользователя',
    )
    def me(self, request, pk=None):
        '''
        Личная страница пользователя.
        Только авторизованные.
        '''
        user = get_object_or_404(CustomUser, email=request.user)
        queryset = CustomUser.objects.filter(email=user)
        serializer = UserSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', ],
        permission_classes=[IsAuthenticated, ],
        name='Подписки на пользователей',
    )
    def subscriptions(self, request, id=None):
        '''
        Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        '''
        user = get_object_or_404(CustomUser, email=request.user)
        queryset = Follow.objects.filter(user=user.id)
        print(queryset)
        serializer = FollowSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        name='Подписаться на пользователя',
    )
    def subscribe(self, request, pk):
        '''
        Осуществляет подписку на пользователя.
        '''
        user = get_object_or_404(CustomUser, email=request.user)
        author = get_object_or_404(CustomUser, id=pk)
        if author == user:
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

        follow = Follow.objects.create(user=user, author=author)
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
        user = get_object_or_404(CustomUser, email=request.user)
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
            user=user,
            author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowsViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по подпискам.
    Отвечает по адресам:
    'users/subscriptions/'
    'users/id/subscribe/'
    '''
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
