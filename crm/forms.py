from django import forms

from clients.models import Client
from insurers.forms import FIELD_CLASS, TenantFormMixin

from .models import Deal, Pipeline, PipelineStage


class PipelineForm(TenantFormMixin, forms.ModelForm):
    class Meta:
        model = Pipeline
        fields = ('name', 'description', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'description': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }


class PipelineStageForm(TenantFormMixin, forms.ModelForm):
    tenant_fields = ('pipeline',)

    class Meta:
        model = PipelineStage
        fields = ('pipeline', 'name', 'color', 'order', 'is_active')
        widgets = {
            'pipeline': forms.Select(attrs={'class': FIELD_CLASS}),
            'name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'color': forms.TextInput(attrs={'class': FIELD_CLASS, 'type': 'color'}),
            'order': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, request=request, **kwargs)
        brokerage = getattr(request, 'brokerage', None)
        self.fields['pipeline'].queryset = Pipeline.objects.for_brokerage(brokerage)


class DealForm(TenantFormMixin, forms.ModelForm):
    tenant_fields = ('pipeline', 'stage', 'client')

    class Meta:
        model = Deal
        fields = ('pipeline', 'stage', 'client', 'title', 'value', 'probability', 'description', 'notes', 'is_active')
        widgets = {
            'pipeline': forms.Select(attrs={'class': FIELD_CLASS}),
            'stage': forms.Select(attrs={'class': FIELD_CLASS}),
            'client': forms.Select(attrs={'class': FIELD_CLASS}),
            'title': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'value': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'probability': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'description': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'notes': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, request=request, **kwargs)
        brokerage = getattr(request, 'brokerage', None)
        self.fields['pipeline'].queryset = Pipeline.objects.for_brokerage(brokerage)
        self.fields['stage'].queryset = PipelineStage.objects.for_brokerage(brokerage)
        self.fields['client'].queryset = Client.objects.for_brokerage(brokerage)
