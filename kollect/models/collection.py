from uuid import uuid4

from django.conf import settings
from django.db import models


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    public = models.BooleanField(default=False)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        app_label = "kollect"
        unique_together = (("name", "created_by"),)

    def __str__(self):
        return self.name
