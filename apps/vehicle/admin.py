from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateTimeRangeFilter

from apps.vehicle.models import FuelConsumptionLog, TractorUnitModel, TrailerModel


@admin.register(TractorUnitModel)
class TractorUnitAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "license_plate", "created_at")
    search_fields = ("license_plate", "company__name")
    list_filter = ("company",)


@admin.register(TrailerModel)
class TrailerAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "license_plate", "created_at")
    search_fields = ("license_plate", "company__name")
    list_filter = ("company",)


@admin.register(FuelConsumptionLog)
class FuelConsumptionLogAdmin(ImportExportModelAdmin):  # "Import" and "Export"
    list_display = (
        "occurred_at",
        "tractor_unit",
        "manifest",
        "driver",
        "distance_km",
        "consumed_fuel_liters",
        "fuel_efficiency",
        "load_status",
        "odometer",
    )

    list_filter = (
        "tractor_unit",
        ("occurred_at", DateTimeRangeFilter),
    )

    search_fields = (
        "description",
        "tractor_unit__license_plate",
        "driver__name",
        "manifest__origin",
        "manifest__destination"
    )

    list_editable = ("distance_km", "consumed_fuel_liters", "load_status", "odometer",)

    def fuel_efficiency(self, obj):
        if obj.consumed_fuel_liters and obj.consumed_fuel_liters > 0:
            ratio = obj.distance_km / obj.consumed_fuel_liters
            return f"{ratio:.2f} km/L"
        return "N/A"

    fuel_efficiency.short_description = "KM/L"  # Column header
