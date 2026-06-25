from django import forms

from insurers.forms import FIELD_CLASS, TenantFormMixin
from policies.models import CoveredItem, Policy

from .models import Claim


class ClaimForm(TenantFormMixin, forms.ModelForm):
    tenant_fields = ('policy', 'covered_item')

    class Meta:
        model = Claim
        fields = ('policy', 'covered_item', 'claim_number', 'status', 'occurrence_date', 'notification_date', 'description', 'amount_requested', 'amount_settled', 'notes', 'is_active')
        widgets = {
            'policy': forms.Select(attrs={'class': FIELD_CLASS}),
            'covered_item': forms.Select(attrs={'class': FIELD_CLASS}),
            'claim_number': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Nº do sinistro'}),
            'status': forms.Select(attrs={'class': FIELD_CLASS}),
            'occurrence_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'notification_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'amount_requested': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'amount_settled': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'notes': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, request=request, **kwargs)
        brokerage = getattr(request, 'brokerage', None)
        self.fields['policy'].queryset = Policy.objects.for_brokerage(brokerage)
        self.fields['covered_item'].queryset = CoveredItem.objects.for_brokerage(brokerage)
