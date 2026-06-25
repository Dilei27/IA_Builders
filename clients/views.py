from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.mixins import TenantQuerysetMixin

from .forms import ClientForm
from .models import Client


class ClientListView(LoginRequiredMixin, TenantQuerysetMixin, ListView):
    context_object_name = 'clients'
    model = Client
    paginate_by = 20
    template_name = 'clients/client_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset


class ClientDetailView(LoginRequiredMixin, TenantQuerysetMixin, DetailView):
    context_object_name = 'client'
    model = Client
    template_name = 'clients/client_detail.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    form_class = ClientForm
    model = Client
    template_name = 'clients/client_form.html'

    def form_valid(self, form):
        if self.request.brokerage is None:
            raise PermissionDenied('User has no brokerage.')

        form.instance.brokerage = self.request.brokerage
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, TenantQuerysetMixin, UpdateView):
    form_class = ClientForm
    model = Client
    template_name = 'clients/client_form.html'


class ClientDeleteView(LoginRequiredMixin, TenantQuerysetMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client_list')
    template_name = 'clients/client_confirm_delete.html'
