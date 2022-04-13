from django import forms


class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(required=True, input_formats=['%d/%m/%Y'])
    check_out = forms.DateTimeField(required=True, input_formats=['%d/%m/%Y'])
