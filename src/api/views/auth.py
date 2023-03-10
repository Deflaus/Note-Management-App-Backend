from typing import Any

from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers.auth import (
    AuthSignInSerializer,
    AuthSignUpSerializer,
    AuthUserOutputSerializer,
)
from core.models import User


class AuthViewSet(GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def get_permissions(self) -> list[BasePermission]:
        if self.action in ("sign_out",):
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (AllowAny,)

        return super().get_permissions()

    @swagger_auto_schema(
        request_body=AuthSignUpSerializer,
        responses={status.HTTP_201_CREATED: AuthUserOutputSerializer()},
        operation_summary="Create new account",
    )
    @action(methods=["POST"], detail=False)
    def sign_up(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = AuthSignUpSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            AuthUserOutputSerializer(instance=user, context={"request": request}).data, status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        request_body=AuthSignInSerializer,
        responses={status.HTTP_200_OK: AuthUserOutputSerializer()},
        operation_summary="Sign in",
    )
    @action(methods=["POST"], detail=False)
    def sign_in(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = AuthSignInSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            AuthUserOutputSerializer(instance=user, context={"request": request}).data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=no_body,
        responses={status.HTTP_204_NO_CONTENT: ""},
        operation_summary="Delete current auth token",
    )
    @action(methods=["POST"], detail=False)
    def sign_out(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
