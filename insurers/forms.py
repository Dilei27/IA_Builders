from django import forms

from .models import Branch, Coverage, Insurer


FIELD_CLASS = 'w-full rounded-xl bg-[#262A34] border border-white/10 px-4 py-3 text-sm text-white outline-none focus:border-blue-500/50'


class TenantModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj)


class TenantFormMixin:
    tenant_fields = ()

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        brokerage = getattr(request, 'brokerage', None)

        for field_name in self.tenant_fields:
            if field_name in self.fields:
                self.fields[field_name].queryset = self.fields[field_name].queryset.for_brokerage(brokerage)


class InsurerForm(TenantFormMixin, forms.ModelForm):
    class Meta:
        model = Insurer
        fields = ('name', 'document', 'website', 'contact_email', 'contact_phone', 'notes', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'document': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'CNPJ'}),
            'website': forms.URLInput(attrs={'class': FIELD_CLASS}),
            'contact_email': forms.EmailInput(attrs={'class': FIELD_CLASS}),
            'contact_phone': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'notes': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }


class BranchForm(TenantFormMixin, forms.ModelForm):
    class Meta:
        model = Branch
        fields = ('name', 'description', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'description': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }


class CoverageForm(TenantFormMixin, forms.ModelForm):
    tenant_fields = ('branch',)

    class Meta:
        model = Coverage
        fields = ('name', 'branch', 'description', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'branch': forms.Select(attrs={'class': FIELD_CLASS}),
            'description': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }
