from typing import Type, Union

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.models import Favorite, ShoppingCart
from users.models import Follow


def create_delete_obj(
        self: viewsets.ModelViewSet,
        pk: int,
        klass: Union[Type[Favorite], Type[ShoppingCart], Type[Follow]],
        error_create_message: str,
        error_delete_message: str,
        field_to_create_or_delete: str):
    source_object = get_object_or_404(self.get_queryset(), id=pk)
    kwargs = {
        'user': self.request.user,
        field_to_create_or_delete: source_object}
    if self.request.method == 'POST':
        if klass.objects.filter(**kwargs).exists():
            response = Response(
                {'errors ': error_create_message},
                status=status.HTTP_400_BAD_REQUEST)
        elif source_object == self.request.user:
            """ На случай подписки на самого себя."""
            response = Response(
                {'errors ': 'Не стоит подписываться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            klass.objects.create(**kwargs)
            serializer = self.get_serializer_class()
            context = self.get_serializer_context()
            response = Response(
                serializer(
                    instance=source_object,
                    context=context).data,
                status=status.HTTP_201_CREATED)
    elif self.request.method == 'DELETE':
        delete_object = klass.objects.filter(**kwargs).first()
        if delete_object is None:
            response = Response(
                {'errors ': error_delete_message},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            delete_object.delete()
            response = Response(status=status.HTTP_204_NO_CONTENT)
    else:
        response = Response(status=status.HTTP_204_NO_CONTENT)
    return response
