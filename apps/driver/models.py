from django.db import models
import uuid
from apps.company.models import Company
from apps.domain.domain_orm import DomainField
from apps.driver.domain import Cpf, Cnh


class CpfField(DomainField):
    def __init__(self, *args, **kwargs):
        self.domain_class = Cpf
        super().__init__(*args, **kwargs)


class CnhField(DomainField):
    def __init__(self, *args, **kwargs):
        self.domain_class = Cnh
        super().__init__(*args, **kwargs)


class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="drivers", null=True, blank=True
    )
    name = models.CharField(max_length=120)
    cpf = CpfField(unique=True, null=True, blank=True)
    cnh = CnhField(unique=True, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
