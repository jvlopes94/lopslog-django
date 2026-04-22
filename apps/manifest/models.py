from django.db import models
import uuid
from apps.company.models import Company


class Manifest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_external = models.CharField(max_length=120, null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, related_name="manifests", null=True, blank=True)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.origin} -> {self.destination}"
