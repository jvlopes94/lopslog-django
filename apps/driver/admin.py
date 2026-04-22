from django.contrib import admin
from apps.driver.models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "name", "cpf", "cnh", "active", "created_at")
    search_fields = ("name", "cpf", "cnh", "company__name")
    list_filter = ("active", "company")
