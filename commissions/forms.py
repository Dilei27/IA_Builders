from django import forms

from insurers.forms import FIELD_CLASS, TenantFormMixin
from policies.models import Policy

from .models import Commission


class CommissionForm(TenantFormMixin, forms.ModelForm):
    tenant_fields = ('policy',)

    class Meta:
        model = Commission
        fields = ('policy', 'commission_type', 'description', 'amount', 'commission_date', 'status', 'notes', 'is_active')
        widgets = {
            'policy': forms.Select(attrs={'class': FIELD_CLASS}),
            'commission_type': forms.Select(attrs={'class': FIELD_CLASS}),
            'description': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Descrição da comissão'}),
            'amount': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'commission_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'status': forms.Select(attrs={'class': FIELD_CLASS}),
            'notes': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, request=request, **kwargs)
        brokerage = getattr(request, 'brokerage', None)
        self.fields['policy'].queryset = Policy.objects.for_brokerage(brokerage)
