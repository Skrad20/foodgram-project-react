from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    FollowsViewSet,
)

v1_router = DefaultRouter()

v1_router.register('users/', UserViewSet, basename='users')
v1_router.register('users/<int: user_id>', UserViewSet, basename='users_id')
v1_router.register('users/me', UserViewSet, basename='me')
v1_router.register(
    'users/subscriptions',
    FollowsViewSet,
    basename='subscriptions'
)
v1_router.register('users/suscribe', FollowsViewSet, basename='suscribe')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path("api/auth/", include("djoser.urls.authtoken")),
]
