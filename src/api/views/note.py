import typing

from django.db.models import QuerySet
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers.note import NoteSerializer, NoteUpdateSerializer
from core.models import Note


class NoteViewSet(GenericViewSet, ListModelMixin, DestroyModelMixin, RetrieveModelMixin, CreateModelMixin):
    queryset = Note.objects.order_by("created_at")
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> typing.Type[serializers.Serializer]:
        if self.action == "partial_update":
            return NoteUpdateSerializer

        return NoteSerializer

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        return super().filter_queryset(queryset).filter(user=self.request.user)

    @swagger_auto_schema(
        request_body=no_body,
        responses={status.HTTP_200_OK: NoteSerializer(many=True)},
        operation_summary="Get own notes",
    )
    def list(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response:
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=no_body,
        responses={status.HTTP_200_OK: NoteSerializer},
        operation_summary="Get own note",
    )
    def retrieve(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=NoteUpdateSerializer,
        responses={status.HTTP_200_OK: NoteSerializer},
        operation_summary="Update own note",
    )
    def partial_update(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=no_body,
        responses={status.HTTP_204_NO_CONTENT: ""},
        operation_summary="Delete own note",
    )
    def destroy(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response:
        return super().destroy(request, *args, **kwargs)
