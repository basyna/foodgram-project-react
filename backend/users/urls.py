from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

router_users = DefaultRouter()
router_users.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_users.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
