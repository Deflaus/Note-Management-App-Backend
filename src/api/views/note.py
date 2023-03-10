import typing

from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers.note import NoteSerializer, NoteUpdateSerializer
from core.models import Note


class NoteViewSet(GenericViewSet, ListModelMixin, DestroyModelMixin, RetrieveModelMixin, CreateModelMixin):
    queryset = Note.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> typing.Type[serializers.Serializer]:
        if self.action == "partial_update":
            return NoteUpdateSerializer

        return NoteSerializer

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        return super().filter_queryset(queryset).filter(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
