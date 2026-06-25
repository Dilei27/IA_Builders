from django.urls import reverse_lazy

from insurers.views import CatalogCreateView, CatalogDeleteView, CatalogDetailView, CatalogUpdateView, SearchableTenantListView

from .forms import ClaimForm
from .models import Claim


class ClaimListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Sinistros',
        'title': 'Sinistros',
        'subtitle': 'Registro de sinistros vinculados a apólices e itens cobertos.',
        'create_url_name': 'claim_create',
        'detail_url_name': 'claim_detail',
    }
    context_object_name = 'objects'
    model = Claim

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')

        if status:
            qs = qs.filter(status=status)

        return qs


class ClaimDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'Sinistro',
        'title': 'Detalhe do sinistro',
        'update_url_name': 'claim_update',
        'delete_url_name': 'claim_delete',
    }
    context_object_name = 'object'
    model = Claim

    def get_details(self):
        claim = self.object
        return (
            ('Nº Sinistro', claim.claim_number or '-'),
            ('Status', claim.get_status_display()),
            ('Apólice', claim.policy),
            ('Item Coberto', claim.covered_item),
            ('Data Ocorrência', claim.occurrence_date.strftime('%d/%m/%Y') if claim.occurrence_date else '-'),
            ('Data Notificação', claim.notification_date.strftime('%d/%m/%Y') if claim.notification_date else '-'),
            ('Descrição', claim.description or 'Sem descrição.'),
            ('Valor Solicitado', f'R$ {claim.amount_requested:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') if claim.amount_requested else '-'),
            ('Valor Liquidado', f'R$ {claim.amount_settled:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') if claim.amount_settled else '-'),
            ('Observações', claim.notes or 'Sem observações.'),
            ('Resumo IA', claim.ai_summary or 'Nenhum resumo gerado.'),
        )


class ClaimCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Sinistros', 'title': 'Novo sinistro', 'list_url_name': 'claim_list'}
    form_class = ClaimForm
    model = Claim


class ClaimUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Sinistros', 'title': 'Editar sinistro', 'list_url_name': 'claim_list'}
    form_class = ClaimForm
    model = Claim


class ClaimDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Sinistros', 'title': 'Excluir sinistro'}
    model = Claim
    success_url = reverse_lazy('claim_list')
