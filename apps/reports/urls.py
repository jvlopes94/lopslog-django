from django.urls import path
from apps.reports.views import fuel_report_page

urlpatterns = [
    path("", fuel_report_page, name="fuel-report-page"),
]
