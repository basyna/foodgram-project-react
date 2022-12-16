from api.paginators import PageLimitPagination
from api.permissions import IsOwnerOrReadOnly
from djoser.serializers import SetPasswordSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Follow, User
from users.serializers import (UserCreateSerializer,
                               UserListOrDetailSerializer,
                               UserSubscriptionsSerializer)


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = PageLimitPagination
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    http_method_names = ['get', 'post', 'delete']

    from api.utils import create_delete_obj

    def get_instance(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'me']:
            return UserListOrDetailSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'set_password':
            return SetPasswordSerializer
        elif self.action in ['subscribe', '']:
            return UserSubscriptionsSerializer

    @action(
        ["get"],
        permission_classes=[IsAuthenticated, ],
        detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(
        ["post"],
        permission_classes=[IsOwnerOrReadOnly, ],
        detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsOwnerOrReadOnly, ], )
    def subscribe(self, request, pk):
        return self.create_delete_obj(
            pk=pk,
            klass=Follow,
            error_create_message='Вы уже подписаны на этого Автора',
            error_delete_message='Вы не подписаны на этого Автора',
            field_to_create_or_delete='author')

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsOwnerOrReadOnly, ], )
    def subscriptions(self, request):
        """Получить на кого пользователь подписан."""
        user = request.user
        queryset = User.objects.filter(
            id__in=(user.follower.values('author_id')))
        pages = self.paginate_queryset(queryset)
        serializer = UserSubscriptionsSerializer(
            pages, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)
