from rest_framework import serializers

from core.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            "pk",
            "name",
            "description",
            "created_at",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
        }

    def validate(self, attrs: dict) -> dict:
        attrs["user"] = self.context["request"].user
        return attrs


class NoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            "pk",
            "name",
            "description",
            "created_at",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
            "name": {"required": False},
        }

    def validate(self, attrs: dict) -> dict:
        attrs["user"] = self.context["request"].user
        return attrs
