from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.mixins import TenantQuerysetMixin

from .forms import BranchForm, CoverageForm, InsurerForm
from .models import Branch, Coverage, Insurer


class TenantCreateMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        if self.request.brokerage is None:
            raise PermissionDenied('User has no brokerage.')

        form.instance.brokerage = self.request.brokerage
        return super().form_valid(form)


class TenantUpdateMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class SearchableTenantListView(LoginRequiredMixin, TenantQuerysetMixin, ListView):
    paginate_by = 20
    template_name = 'catalog/object_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.catalog_context)
        return context


class CatalogDetailView(LoginRequiredMixin, TenantQuerysetMixin, DetailView):
    template_name = 'catalog/object_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.catalog_context)
        context['details'] = self.get_details()
        return context


class CatalogCreateView(LoginRequiredMixin, TenantCreateMixin, CreateView):
    template_name = 'catalog/object_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.catalog_context)
        return context


class CatalogUpdateView(LoginRequiredMixin, TenantUpdateMixin, TenantQuerysetMixin, UpdateView):
    template_name = 'catalog/object_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.catalog_context)
        return context


class CatalogDeleteView(LoginRequiredMixin, TenantQuerysetMixin, DeleteView):
    template_name = 'catalog/object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.catalog_context)
        return context


class InsurerListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Seguradoras',
        'title': 'Seguradoras',
        'subtitle': 'Cadastro de seguradoras por corretora.',
        'create_url_name': 'insurer_create',
        'detail_url_name': 'insurer_detail',
    }
    context_object_name = 'objects'
    model = Insurer


class InsurerDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'Seguradora',
        'title': 'Detalhe da seguradora',
        'update_url_name': 'insurer_update',
        'delete_url_name': 'insurer_delete',
    }
    context_object_name = 'object'
    model = Insurer

    def get_details(self):
        insurer = self.object
        return (
            ('Documento', insurer.document or '-'),
            ('Site', insurer.website or '-'),
            ('Email', insurer.contact_email or '-'),
            ('Telefone', insurer.contact_phone or '-'),
            ('Status', 'Ativa' if insurer.is_active else 'Inativa'),
            ('Observações', insurer.notes or 'Sem observações.'),
        )


class InsurerCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Seguradoras', 'title': 'Nova seguradora', 'list_url_name': 'insurer_list'}
    form_class = InsurerForm
    model = Insurer


class InsurerUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Seguradoras', 'title': 'Editar seguradora', 'list_url_name': 'insurer_list'}
    form_class = InsurerForm
    model = Insurer


class InsurerDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Seguradoras', 'title': 'Excluir seguradora'}
    model = Insurer
    success_url = reverse_lazy('insurer_list')


class BranchListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Ramos',
        'title': 'Ramos de seguro',
        'subtitle': 'Categorias comerciais usadas em propostas, apólices e itens.',
        'create_url_name': 'branch_create',
        'detail_url_name': 'branch_detail',
    }
    context_object_name = 'objects'
    model = Branch


class BranchDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'Ramo',
        'title': 'Detalhe do ramo',
        'update_url_name': 'branch_update',
        'delete_url_name': 'branch_delete',
    }
    context_object_name = 'object'
    model = Branch

    def get_details(self):
        branch = self.object
        return (
            ('Status', 'Ativo' if branch.is_active else 'Inativo'),
            ('Descrição', branch.description or 'Sem descrição.'),
        )


class BranchCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Ramos', 'title': 'Novo ramo', 'list_url_name': 'branch_list'}
    form_class = BranchForm
    model = Branch


class BranchUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Ramos', 'title': 'Editar ramo', 'list_url_name': 'branch_list'}
    form_class = BranchForm
    model = Branch


class BranchDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Ramos', 'title': 'Excluir ramo'}
    model = Branch
    success_url = reverse_lazy('branch_list')


class CoverageListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Coberturas',
        'title': 'Coberturas',
        'subtitle': 'Coberturas disponíveis por ramo e corretora.',
        'create_url_name': 'coverage_create',
        'detail_url_name': 'coverage_detail',
    }
    context_object_name = 'objects'
    model = Coverage


class CoverageDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'Cobertura',
        'title': 'Detalhe da cobertura',
        'update_url_name': 'coverage_update',
        'delete_url_name': 'coverage_delete',
    }
    context_object_name = 'object'
    model = Coverage

    def get_details(self):
        coverage = self.object
        return (
            ('Ramo', coverage.branch),
            ('Status', 'Ativa' if coverage.is_active else 'Inativa'),
            ('Descrição', coverage.description or 'Sem descrição.'),
        )


class CoverageCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Coberturas', 'title': 'Nova cobertura', 'list_url_name': 'coverage_list'}
    form_class = CoverageForm
    model = Coverage


class CoverageUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Coberturas', 'title': 'Editar cobertura', 'list_url_name': 'coverage_list'}
    form_class = CoverageForm
    model = Coverage


class CoverageDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Coberturas', 'title': 'Excluir cobertura'}
    model = Coverage
    success_url = reverse_lazy('coverage_list')
