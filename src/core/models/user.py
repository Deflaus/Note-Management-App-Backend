from django.contrib.auth.models import AbstractUser

from core.models.mixins import CreatedAtUpdatedAtMixin


class User(AbstractUser, CreatedAtUpdatedAtMixin):
    REQUIRED_FIELDS: list[str] = []

    def __str__(self):
        return f"User {self.username}"
