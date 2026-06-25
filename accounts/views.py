from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import OnboardingForm


class LandingView(TemplateView):
    template_name = 'accounts/landing.html'


class SignupView(FormView):
    form_class = OnboardingForm
    success_url = reverse_lazy('dashboard')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        brokerage, user = form.save()
        login(self.request, user)
        messages.success(self.request, f'Conta criada para {brokerage.legal_name}.')
        return super().form_valid(form)
