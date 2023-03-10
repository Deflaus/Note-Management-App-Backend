import typing

from django.contrib.auth.backends import ModelBackend
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from api.constants import WRONG_PASSWORD_OR_USERNAME
from api.serializers.user import UserSerializer
from api.utils import check_password_complexity
from core.models import User


class AuthSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")

    def validate(self, attrs: dict) -> dict:
        check_password_complexity(attrs["password"])

        return attrs

    def create(self, validated_data: dict) -> User:
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user


class AuthUserOutputSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("token",)  # type: ignore

    def get_token(self, obj: User) -> str:
        tokens = Token.objects.get_or_create(user=obj)

        return tokens[0].key


class AuthSignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs: dict) -> dict:
        user = ModelBackend().authenticate(
            request=self.context["request"], username=attrs["username"], password=attrs["password"]
        )
        if not user:
            raise AuthenticationFailed(WRONG_PASSWORD_OR_USERNAME)

        attrs["user"] = user
        return attrs

    def create(self, validated_data: dict) -> User:
        return validated_data["user"]

    def update(self, instance: typing.Any, validated_data: dict):
        raise NotImplementedError
