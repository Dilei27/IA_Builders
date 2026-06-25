from django import forms

from .models import Attachment, ALLOWED_EXTENSIONS


class UploadForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('content_type', 'object_id', 'file', 'description')
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
            'description': forms.TextInput(attrs={'class': 'w-full rounded-xl bg-[#262A34] border border-white/10 px-4 py-3 text-sm text-white outline-none focus:border-blue-500/50', 'placeholder': 'Descrição opcional'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file:
            ext = f'.{file.name.split(".")[-1].lower()}'

            if ext not in ALLOWED_EXTENSIONS:
                raise forms.ValidationError(f'Tipo de arquivo "{ext}" não permitido. Permitidos: {", ".join(sorted(ALLOWED_EXTENSIONS))}.')

        return file
