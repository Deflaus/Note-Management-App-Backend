from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "is_active",
        )
        extra_kwargs = {
            "is_active": {"read_only": True},
        }
