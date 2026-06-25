from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class EmailAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True, 'autocomplete': 'email'}),
    )
