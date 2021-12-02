from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    FollowsViewSet,
    CustomAuthToken,
    Logout
)
v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('users/subscriptions', FollowsViewSet.as_view({'get': 'list'})),
    path('auth/token/login/', CustomAuthToken.as_view()),
    path('auth/token/logout/', Logout.as_view()),
]
