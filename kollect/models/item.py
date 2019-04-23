from uuid import uuid4

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=256)
    collection = models.ForeignKey(
        "kollect.Collection", on_delete=models.CASCADE, related_name="items"
    )
    data = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        app_label = "kollect"

    def __str__(self):
        return self.name
