from django.contrib import admin
from apps.company.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cnpj", "active", "created_at")
    search_fields = ("name", "cnpj")
    list_filter = ("active",)
