from django.db import models
import uuid
from apps.company.models import Company
from apps.domain.domain_orm import DomainField
from apps.driver.models import Driver
from apps.vehicle.domain import LicensePlate
from apps.manifest.models import Manifest


class LicensePlateField(DomainField):
    def __init__(self, *args, **kwargs):
        self.domain_class = LicensePlate
        super().__init__(*args, **kwargs)


class TractorUnitModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="tractor_units", null=True, blank=True
    )
    license_plate = LicensePlateField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.license_plate)


class TrailerModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="trailers", null=True, blank=True
    )
    license_plate = LicensePlateField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.license_plate)


class FuelConsumptionLog(models.Model):
    class LoadStatus(models.TextChoices):
        LOADED = "LOADED", "C"
        EMPTY = "EMPTY", "V"
        LOADED_THEN_EMPTY = "LOADED_THEN_EMPTY", "C/V"
        EMPTY_THEN_LOADED = "EMPTY_THEN_LOADED", "V/C"

    manifest = models.ForeignKey(
        Manifest, on_delete=models.SET_NULL, null=True, blank=True, related_name="fuel_logs"
    )
    tractor_unit = models.ForeignKey(
        TractorUnitModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="fuel_logs"
    )
    driver = models.ForeignKey(
        Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name="fuel_logs"
    )
    occurred_at = models.DateTimeField()
    description = models.CharField(max_length=255)
    distance_km = models.PositiveIntegerField()
    consumed_fuel_liters = models.DecimalField(max_digits=10, decimal_places=2)
    load_status = models.CharField(max_length=20, choices=LoadStatus.choices)
    odometer = models.PositiveIntegerField(help_text="Vehicle odometer after fueling/event")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["occurred_at", "id"]

    def __str__(self):
        return self.description
