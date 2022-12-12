from datetime import datetime as dt

from django.db.models import F, Sum
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response

from api.models import Amount, Favorite, Ingredient, Recipe, ShoppingCart, Tag
from api.paginators import PageLimitPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeSerializer,
                             TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        search_field = self.request.query_params.get('name').lower()
        if search_field:
            queryset = queryset.filter(name__startswith=search_field)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = PageLimitPagination
    from api.utils import create_delete_obj

    def get_queryset(self):
        queryset = Recipe.objects
        tags = self.request.query_params.getlist('tags')
        user = self.request.user
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        queryset = queryset.add_user_annotations(user.pk)
        if self.request.query_params.get('is_favorited'):
            queryset = queryset.filter(is_favorited=True)
        if self.request.query_params.get('is_in_shopping_cart'):
            queryset = queryset.filter(is_in_shopping_cart=True)
        if self.request.query_params.get('author'):
            queryset = queryset.filter(
                author_id=self.request.query_params.get('author'))
        return queryset

    def get_permissions(self):
        if self.action not in SAFE_METHODS:
            return [IsOwnerOrReadOnly()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        elif self.action in ('shopping_cart', 'favorite'):
            return FavoriteSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete']
        )
    def shopping_cart(self, request, pk):
        return self.create_delete_obj(
            pk=pk,
            klass=ShoppingCart,
            error_create_message='Этот рецепт уже есть в Корзине',
            error_delete_message='Этот рецепт не найден в Корзине',
            field_to_create_or_delete='recipe'
        )

    @action(
        detail=True,
        methods=['post', 'delete']
        )
    def favorite(self, request, pk):
        return self.create_delete_obj(
            pk=pk,
            klass=Favorite,
            error_create_message='Этот рецепт уже есть в Избранном',
            error_delete_message='Этот рецепт не найден в Избранном',
            field_to_create_or_delete='recipe'
        )

    @action(
        detail=False,
        methods=['get']
        )
    def download_shopping_cart(self, request):
        """Качаем список с ингредиентами."""
        user = request.user
        if not user.shopping_cart.all().exists():
            return Response(
                {'error': 'Корзина пуста'},
                status=status.HTTP_400_BAD_REQUEST)
        ingredients = Amount.objects.filter(
            recipe__in=(user.shopping_cart.values('recipe_id'))
        ).values(
            shop_ingredient=F('ingredient__name'),
            shop_measure=F('ingredient__measurement_unit')
        ).annotate(amount=Sum('amount'))
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = (
                f'Список покупок для пользователя: {user.first_name}\n'
                f'{dt.now().strftime("%H:%M  %m.%d.%Y")}\n\n'
                )
        for ing in ingredients:
            shopping_list += (
                f'{ing["shop_ingredient"]}: {ing["amount"]}'
                f' {ing["shop_measure"]}\n'
            )
        shopping_list += '\n\nПосчитано в Foodgram'
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
