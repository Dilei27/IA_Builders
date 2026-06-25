import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from core.models import Brokerage


class OnboardingForm(forms.Form):
    legal_name = forms.CharField(label='Razão Social', max_length=255)
    trade_name = forms.CharField(label='Nome Fantasia', max_length=255, required=False)
    cnpj = forms.CharField(label='CNPJ', max_length=18)
    brokerage_email = forms.EmailField(label='Email da corretora', required=False)
    full_name = forms.CharField(label='Nome do responsável', max_length=255)
    email = forms.EmailField(label='Email de acesso')
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput)
    plan = forms.ChoiceField(label='Plano', choices=Brokerage.Plan.choices, initial=Brokerage.Plan.FREE)

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        digits = re.sub(r'\D', '', cnpj)

        if len(digits) != 14:
            raise forms.ValidationError('Informe um CNPJ com 14 dígitos.')

        if Brokerage.objects.filter(cnpj=digits).exists():
            raise forms.ValidationError('Já existe uma corretora cadastrada com este CNPJ.')

        return digits

    def clean_email(self):
        email = self.cleaned_data['email']
        user_model = get_user_model()

        if user_model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Já existe um usuário cadastrado com este email.')

        return email

    def clean_plan(self):
        plan = self.cleaned_data['plan']

        if plan != Brokerage.Plan.FREE:
            raise forms.ValidationError('Apenas o plano free está habilitado neste momento.')

        return plan

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'As senhas não conferem.')

        if password1:
            try:
                validate_password(password1)
            except forms.ValidationError as error:
                self.add_error('password1', error)

        return cleaned_data

    @transaction.atomic
    def save(self):
        brokerage = Brokerage.objects.create(
            cnpj=self.cleaned_data['cnpj'],
            legal_name=self.cleaned_data['legal_name'],
            trade_name=self.cleaned_data['trade_name'],
            email=self.cleaned_data['brokerage_email'],
            plan=Brokerage.Plan.FREE,
        )
        user_model = get_user_model()
        user = user_model.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            full_name=self.cleaned_data['full_name'],
            brokerage=brokerage,
            role=user_model.Role.OWNER,
        )
        return brokerage, user
