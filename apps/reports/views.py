from django.shortcuts import render
from apps.reports.forms import FuelReportForm
from apps.reports.services import build_fuel_report_data, build_pdf_response


def fuel_report_page(request):
    if request.method == "POST":
        form = FuelReportForm(request.POST)
        if form.is_valid():
            try:
                report = build_fuel_report_data(
                    tractor_unit=form.cleaned_data["tractor_unit"],
                    start_date=form.cleaned_data["start_date"],
                    end_date=form.cleaned_data["end_date"],
                    initial_km=form.cleaned_data["initial_km"],
                )
                return build_pdf_response(report)
            except RuntimeError as exc:
                form.add_error(None, str(exc))
    else:
        form = FuelReportForm()
    return render(request, "reports/fuel_report_form.html", {"form": form})
