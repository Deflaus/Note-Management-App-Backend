from django.db import models

from core.models.mixins import CreatedAtUpdatedAtMixin


class Note(CreatedAtUpdatedAtMixin):
    user: models.ForeignKey = models.ForeignKey("User", on_delete=models.CASCADE, related_name="notes")
    name: models.CharField = models.CharField(max_length=255, blank=False, null=False)
    description: models.TextField = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Note #{self.pk}"
