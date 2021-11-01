from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import (
    permissions,
    serializers,
    viewsets,
    filters,
    mixins,
    status,
)
from .serializers import (
    UserSerializer,
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

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, ]
    )
    def set_password(self, request, pk=None):
        '''
        Реализует механизм смены пароля.
        Только POST запросы и только авторизованные.
        '''
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'Пароль установлен'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['get'],
        permission_classes=[IsAuthenticated, ]
    )

    def set_password(self, request, pk=None):
        '''
        Личная страница пользователя.
        Ттолько авторизованные.
        '''
        pass


class FollowsViewSet(viewsets.ModelViewSet):
    '''
    Возвращает данные по подпискам.
    Отвечает по адресам:
    'users/subscriptions/'
    'users/id/subscribe/'
    '''
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, ]
    )
    def subscriptions(self, request, pk=None):
        '''
        Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        '''
        pass

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, ]
    )
    def subscribe(self, request, pk=None):
        '''
        Реализует подписку и отписку на пользователя.
        Доступно только авторизованным пользователям.
        '''
        pass
