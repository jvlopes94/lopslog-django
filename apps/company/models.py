import uuid
from django.db import models

from apps.company.domain import Cnpj
from apps.domain.domain_orm import DomainField


class CnpjField(DomainField):
    def __init__(self, *args, **kwargs):
        self.domain_class = Cnpj
        super().__init__(*args, **kwargs)


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, unique=True)
    cnpj = CnpjField(unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return self.name
