from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomAuthToken, Logout, UserViewSet

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/token/login/', CustomAuthToken.as_view(), name='login_user'),
    path('auth/token/logout/', Logout.as_view(), name='logout_user'),
]
