from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from recipes.pagination import CustomPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import (
    get_object_or_404,
)
from rest_framework import (
    viewsets,
    status,
)
from .serializers import (
    UserSerializer,
    CustomUserCreateSerializer,
    FollowSerializer,
    PasswordSerializer,
    AuthTokenSerializer,
    FollowSerializerView,
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
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, )
    pagination_class = CustomPagination
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
        detail=True,
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
        permission_classes=[IsAuthenticated],
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


class FollowsViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по подпискам.
    Отвечает по адресам:
    'users/subscriptions/'
    '''
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'author_id'

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        author = get_object_or_404(CustomUser, pk=self.kwargs.get('author_id'))
        serializer.save(user=self.request.user, author=author)

    def perform_destroy(self, instance):
        user = self.request.user
        author = get_object_or_404(CustomUser, pk=self.kwargs.get('author_id'))
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
