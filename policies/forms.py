from django import forms

from clients.models import Client
from insurers.forms import FIELD_CLASS, TenantFormMixin
from insurers.models import Branch, Coverage, Insurer

from .models import CoveredItem, Endorsement, Policy, Proposal


class CoveredItemForm(TenantFormMixin, forms.ModelForm):
    tenant_fields = ('client', 'branch')

    class Meta:
        model = CoveredItem
        fields = ('client', 'branch', 'item_type', 'name', 'identifier', 'description', 'is_active')
        widgets = {
            'client': forms.Select(attrs={'class': FIELD_CLASS}),
            'branch': forms.Select(attrs={'class': FIELD_CLASS}),
            'item_type': forms.Select(attrs={'class': FIELD_CLASS}),
            'name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'identifier': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Placa, chassi, matrícula ou referência'}),
            'description': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, request=request, **kwargs)
        brokerage = getattr(request, 'brokerage', None)
        self.fields['client'].queryset = Client.objects.for_brokerage(brokerage)
        self.fields['branch'].queryset = Branch.objects.for_brokerage(brokerage)


class ProposalForm(TenantFormMixin, forms.ModelForm):
    tenant_fields = ('client', 'branch', 'insurer')

    class Meta:
        model = Proposal
        fields = ('proposal_number', 'client', 'branch', 'insurer', 'coverages', 'covered_items', 'status', 'start_date', 'end_date', 'premium_value', 'insured_value', 'notes', 'is_active')
        widgets = {
            'proposal_number': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Número da proposta'}),
            'client': forms.Select(attrs={'class': FIELD_CLASS}),
            'branch': forms.Select(attrs={'class': FIELD_CLASS}),
            'insurer': forms.Select(attrs={'class': FIELD_CLASS}),
            'coverages': forms.SelectMultiple(attrs={'class': FIELD_CLASS}),
            'covered_items': forms.SelectMultiple(attrs={'class': FIELD_CLASS}),
            'status': forms.Select(attrs={'class': FIELD_CLASS}),
            'start_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'premium_value': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'insured_value': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'notes': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, request=request, **kwargs)
        brokerage = getattr(request, 'brokerage', None)
        self.fields['client'].queryset = Client.objects.for_brokerage(brokerage)
        self.fields['branch'].queryset = Branch.objects.for_brokerage(brokerage)
        self.fields['insurer'].queryset = Insurer.objects.for_brokerage(brokerage)
        self.fields['coverages'].queryset = Coverage.objects.for_brokerage(brokerage)
        self.fields['covered_items'].queryset = CoveredItem.objects.for_brokerage(brokerage)


class PolicyForm(TenantFormMixin, forms.ModelForm):
    tenant_fields = ('client', 'branch', 'insurer', 'proposal')

    class Meta:
        model = Policy
        fields = ('policy_number', 'proposal', 'client', 'branch', 'insurer', 'coverages', 'covered_items', 'status', 'start_date', 'end_date', 'premium_value', 'insured_value', 'notes', 'is_active')
        widgets = {
            'policy_number': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Número da apólice'}),
            'proposal': forms.Select(attrs={'class': FIELD_CLASS}),
            'client': forms.Select(attrs={'class': FIELD_CLASS}),
            'branch': forms.Select(attrs={'class': FIELD_CLASS}),
            'insurer': forms.Select(attrs={'class': FIELD_CLASS}),
            'coverages': forms.SelectMultiple(attrs={'class': FIELD_CLASS}),
            'covered_items': forms.SelectMultiple(attrs={'class': FIELD_CLASS}),
            'status': forms.Select(attrs={'class': FIELD_CLASS}),
            'start_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'premium_value': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'insured_value': forms.NumberInput(attrs={'class': FIELD_CLASS}),
            'notes': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, request=request, **kwargs)
        brokerage = getattr(request, 'brokerage', None)
        self.fields['proposal'].queryset = Proposal.objects.for_brokerage(brokerage)
        self.fields['client'].queryset = Client.objects.for_brokerage(brokerage)
        self.fields['branch'].queryset = Branch.objects.for_brokerage(brokerage)
        self.fields['insurer'].queryset = Insurer.objects.for_brokerage(brokerage)
        self.fields['coverages'].queryset = Coverage.objects.for_brokerage(brokerage)
        self.fields['covered_items'].queryset = CoveredItem.objects.for_brokerage(brokerage)


class EndorsementForm(TenantFormMixin, forms.ModelForm):
    tenant_fields = ('policy',)

    class Meta:
        model = Endorsement
        fields = ('policy', 'endorsement_number', 'endorsement_type', 'description', 'effective_date', 'notes', 'is_active')
        widgets = {
            'policy': forms.Select(attrs={'class': FIELD_CLASS}),
            'endorsement_number': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Nº do endosso'}),
            'endorsement_type': forms.Select(attrs={'class': FIELD_CLASS}),
            'description': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'effective_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, request=request, **kwargs)
        brokerage = getattr(request, 'brokerage', None)
        self.fields['policy'].queryset = Policy.objects.for_brokerage(brokerage)
