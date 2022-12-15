from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet

router_api = DefaultRouter()
router_api.register('recipes', RecipeViewSet, basename='recipes')
router_api.register('tags', TagViewSet, basename='tags')
router_api.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router_api.urls)),
    path('', include('users.urls')),
]
