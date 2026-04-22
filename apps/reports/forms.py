from django import forms
from apps.vehicle.models import TractorUnitModel


class FuelReportForm(forms.Form):
    tractor_unit = forms.ModelChoiceField(
        queryset=TractorUnitModel.objects.all(),
        required=True,
        label="License plate",
    )
    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={"type": "date"}))
    initial_km = forms.IntegerField(required=True, min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date must be before end date.")
        return cleaned
