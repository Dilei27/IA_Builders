from django.urls import reverse_lazy

from insurers.views import CatalogCreateView, CatalogDeleteView, CatalogDetailView, CatalogUpdateView, SearchableTenantListView

from .forms import RenewalForm
from .models import Renewal


class RenewalListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Renovações',
        'title': 'Renovações',
        'subtitle': 'Renovações de apólices com vencimentos e status.',
        'create_url_name': 'renewal_create',
        'detail_url_name': 'renewal_detail',
    }
    context_object_name = 'objects'
    model = Renewal

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')

        if status:
            qs = qs.filter(status=status)

        return qs


class RenewalDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'Renovação',
        'title': 'Detalhe da renovação',
        'update_url_name': 'renewal_update',
        'delete_url_name': 'renewal_delete',
    }
    context_object_name = 'object'
    model = Renewal

    def get_details(self):
        renewal = self.object
        return (
            ('Nº Renovação', renewal.renewal_number or '-'),
            ('Status', renewal.get_status_display()),
            ('Apólice', renewal.policy),
            ('Fim Vigência Anterior', renewal.previous_end_date.strftime('%d/%m/%Y') if renewal.previous_end_date else '-'),
            ('Nova Vigência Início', renewal.new_start_date.strftime('%d/%m/%Y') if renewal.new_start_date else '-'),
            ('Nova Vigência Fim', renewal.new_end_date.strftime('%d/%m/%Y') if renewal.new_end_date else '-'),
            ('Prêmio', f'R$ {renewal.premium_value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') if renewal.premium_value else '-'),
            ('Observações', renewal.notes or 'Sem observações.'),
        )


class RenewalCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Renovações', 'title': 'Nova renovação', 'list_url_name': 'renewal_list'}
    form_class = RenewalForm
    model = Renewal


class RenewalUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Renovações', 'title': 'Editar renovação', 'list_url_name': 'renewal_list'}
    form_class = RenewalForm
    model = Renewal


class RenewalDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Renovações', 'title': 'Excluir renovação'}
    model = Renewal
    success_url = reverse_lazy('renewal_list')
