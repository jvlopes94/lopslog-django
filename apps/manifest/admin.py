from django.contrib import admin

from apps.manifest.models import Manifest


@admin.register(Manifest)
class TractorUnitAdmin(admin.ModelAdmin):
    list_display = ("id", "id_external", "company", "origin", "destination")
    list_editable = ("origin", "destination")
