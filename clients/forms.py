from django import forms

from .models import Client


FIELD_CLASS = 'w-full rounded-xl bg-[#262A34] border border-white/10 px-4 py-3 text-sm text-white outline-none focus:border-blue-500/50'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'person_type',
            'name',
            'document',
            'email',
            'phone',
            'address_line',
            'city',
            'state',
            'postal_code',
            'notes',
            'is_active',
        )

        widgets = {
            'person_type': forms.Select(attrs={'class': FIELD_CLASS}),
            'name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'document': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'CPF ou CNPJ'}),
            'email': forms.EmailInput(attrs={'class': FIELD_CLASS}),
            'phone': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'address_line': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'city': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'state': forms.TextInput(attrs={'class': FIELD_CLASS, 'maxlength': 2}),
            'postal_code': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'notes': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded bg-[#262A34] border-white/10'}),
        }

    def clean_state(self):
        return self.cleaned_data['state'].upper()
