from django import forms

from insurers.forms import FIELD_CLASS, TenantFormMixin
from policies.models import Policy

from .models import Renewal


class RenewalForm(TenantFormMixin, forms.ModelForm):
    tenant_fields = ('policy',)

    class Meta:
        model = Renewal
        fields = ('policy', 'renewal_number', 'status', 'previous_end_date', 'new_start_date', 'new_end_date', 'premium_value', 'notes', 'is_active')
        widgets = {
            'policy': forms.Select(attrs={'class': FIELD_CLASS}),
            'renewal_number': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Nº da renovação'}),
            'status': forms.Select(attrs={'class': FIELD_CLASS}),
            'previous_end_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'new_start_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'new_end_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'premium_value': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'notes': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, request=request, **kwargs)
        brokerage = getattr(request, 'brokerage', None)
        self.fields['policy'].queryset = Policy.objects.for_brokerage(brokerage)
