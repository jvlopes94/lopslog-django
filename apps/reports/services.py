from dataclasses import dataclass
from datetime import datetime, time
from decimal import Decimal
from io import BytesIO
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
from apps.vehicle.models import FuelConsumptionLog, TractorUnitModel


@dataclass
class FuelReportData:
    tractor_unit: TractorUnitModel
    start_date: datetime.date
    end_date: datetime.date
    initial_km: int
    logs: list
    total_km: int
    total_liters: Decimal
    average_km_per_liter: Decimal
    final_odometer: int
    km_balance: int


def build_fuel_report_data(tractor_unit, start_date, end_date, initial_km) -> FuelReportData:
    start_dt = timezone.make_aware(datetime.combine(start_date, time.min))
    end_dt = timezone.make_aware(datetime.combine(end_date, time.max))
    logs_qs = FuelConsumptionLog.objects.filter(
        tractor_unit=tractor_unit, occurred_at__range=(start_dt, end_dt)
    ).select_related("driver")
    logs = list(logs_qs)

    totals = logs_qs.aggregate(
        total_km=Sum("distance_km"),
        total_liters=Sum("consumed_fuel_liters"),
    )
    total_km = totals["total_km"] or 0
    total_liters = totals["total_liters"] or Decimal("0")
    average = Decimal("0")
    if total_liters > 0:
        average = Decimal(total_km) / total_liters
    final_odometer = initial_km + total_km
    km_balance = total_km - 10000

    return FuelReportData(
        tractor_unit=tractor_unit,
        start_date=start_date,
        end_date=end_date,
        initial_km=initial_km,
        logs=logs,
        total_km=total_km,
        total_liters=total_liters,
        average_km_per_liter=average,
        final_odometer=final_odometer,
        km_balance=km_balance,
    )


def render_fuel_report_pdf(report: FuelReportData) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.pdfgen import canvas
    except Exception as exc:
        raise RuntimeError("Missing dependency: install reportlab to generate PDFs.") from exc

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    y = height - 40
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(30, y, "CONTROLE DE KMS RODADOS E CONSUMO DE COMBUSTIVEL")
    y -= 30
    pdf.setFont("Helvetica", 10)
    pdf.drawString(30, y, f"Empresa: {report.tractor_unit.company.name}")
    pdf.drawString(260, y, f"CNPJ {report.tractor_unit.company.cnpj}")
    y -= 18
    pdf.drawString(30, y, f"Placa: {report.tractor_unit.license_plate}")
    pdf.drawString(190, y, f"Periodo: {report.start_date:%d/%m/%Y} - {report.end_date:%d/%m/%Y}")
    y -= 20
    pdf.drawString(30, y, f"KM inicial: {report.initial_km}")
    pdf.drawString(190, y, f"Total KMs rodados: {report.total_km}")
    pdf.drawString(380, y, f"Total litragem: {report.total_liters:.2f}")
    pdf.drawString(540, y, f"Media total: {report.average_km_per_liter:.2f}")
    y -= 20
    pdf.drawString(30, y, f"Saldo KM (quota 10.000): {report.km_balance}")
    pdf.drawString(260, y, f"Espelhamento final: {report.final_odometer}")
    y -= 25

    headers = ["Data", "Descricao", "KMs", "Litragem", "Media Km/L", "Carregado/Vazio", "Espelhamento"]
    x_positions = [30, 95, 380, 450, 520, 600, 700]
    pdf.setFont("Helvetica-Bold", 9)
    for idx, header in enumerate(headers):
        pdf.drawString(x_positions[idx], y, header)
    y -= 15
    pdf.setFont("Helvetica", 9)

    current_odometer = report.initial_km
    for log in report.logs:
        if y < 40:
            pdf.showPage()
            y = height - 40
            pdf.setFont("Helvetica", 9)
        row_avg = Decimal("0")
        if log.consumed_fuel_liters > 0:
            row_avg = Decimal(log.distance_km) / log.consumed_fuel_liters
        current_odometer += log.distance_km
        status = "C" if log.load_status == FuelConsumptionLog.LoadStatus.LOADED else "V"
        if log.load_status == FuelConsumptionLog.LoadStatus.LOADED_THEN_EMPTY:
            status = "C/V"
        if log.load_status == FuelConsumptionLog.LoadStatus.EMPTY_THEN_LOADED:
            status = "V/C"
        pdf.drawString(x_positions[0], y, log.occurred_at.strftime("%d/%m/%Y"))
        pdf.drawString(x_positions[1], y, log.description[:45])
        pdf.drawRightString(x_positions[2] + 45, y, str(log.distance_km))
        pdf.drawRightString(x_positions[3] + 45, y, f"{log.consumed_fuel_liters:.2f}")
        pdf.drawRightString(x_positions[4] + 55, y, f"{row_avg:.2f}")
        pdf.drawString(x_positions[5], y, status)
        pdf.drawRightString(x_positions[6] + 55, y, str(current_odometer))
        y -= 14

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def build_pdf_response(report: FuelReportData) -> HttpResponse:
    content = render_fuel_report_pdf(report)
    filename = f"fuel-report-{report.tractor_unit.license_plate}-{report.start_date:%Y%m}.pdf"
    response = HttpResponse(content, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
