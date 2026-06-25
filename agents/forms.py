from django import forms

from insurers.forms import FIELD_CLASS, TenantFormMixin

from .models import Agent, Producer


class AgentForm(TenantFormMixin, forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('name', 'document', 'email', 'phone', 'commission_rate', 'notes', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'document': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'CPF ou CNPJ'}),
            'email': forms.EmailInput(attrs={'class': FIELD_CLASS}),
            'phone': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'commission_rate': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'notes': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }


class ProducerForm(TenantFormMixin, forms.ModelForm):
    tenant_fields = ('agent',)

    class Meta:
        model = Producer
        fields = ('agent', 'name', 'document', 'email', 'phone', 'commission_rate', 'notes', 'is_active')
        widgets = {
            'agent': forms.Select(attrs={'class': FIELD_CLASS}),
            'name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'document': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'CPF'}),
            'email': forms.EmailInput(attrs={'class': FIELD_CLASS}),
            'phone': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'commission_rate': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'notes': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, request=request, **kwargs)
        brokerage = getattr(request, 'brokerage', None)
        self.fields['agent'].queryset = Agent.objects.for_brokerage(brokerage)
