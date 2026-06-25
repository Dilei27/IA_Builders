from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import ListView

from base.mixins import TenantQuerysetMixin
from insurers.views import CatalogCreateView, CatalogDeleteView, CatalogDetailView, CatalogUpdateView, SearchableTenantListView

from .forms import CommissionForm
from .models import Commission


class CommissionListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Comissões',
        'title': 'Comissões',
        'subtitle': 'Comissões recebidas e repassadas por corretora.',
        'create_url_name': 'commission_create',
        'detail_url_name': 'commission_detail',
    }
    context_object_name = 'objects'
    model = Commission

    def get_queryset(self):
        qs = super().get_queryset()
        ct = self.request.GET.get('type')

        if ct:
            qs = qs.filter(commission_type=ct)

        status = self.request.GET.get('status')

        if status:
            qs = qs.filter(status=status)

        return qs


class CommissionDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'Comissão',
        'title': 'Detalhe da comissão',
        'update_url_name': 'commission_update',
        'delete_url_name': 'commission_delete',
    }
    context_object_name = 'object'
    model = Commission

    def get_details(self):
        c = self.object
        return (
            ('Tipo', c.get_commission_type_display()),
            ('Apólice', c.policy),
            ('Descrição', c.description or '-'),
            ('Valor', f'R$ {c.amount:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')),
            ('Data', c.commission_date.strftime('%d/%m/%Y') if c.commission_date else '-'),
            ('Status', c.get_status_display()),
            ('Observações', c.notes or 'Sem observações.'),
        )


class CommissionCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Comissões', 'title': 'Nova comissão', 'list_url_name': 'commission_list'}
    form_class = CommissionForm
    model = Commission


class CommissionUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Comissões', 'title': 'Editar comissão', 'list_url_name': 'commission_list'}
    form_class = CommissionForm
    model = Commission


class CommissionDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Comissões', 'title': 'Excluir comissão'}
    model = Commission
    success_url = reverse_lazy('commission_list')


class RepasseListView(LoginRequiredMixin, TenantQuerysetMixin, ListView):
    context_object_name = 'objects'
    model = Commission
    template_name = 'commissions/repasse_list.html'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(commission_type=Commission.CommissionType.PASSED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brokerage = getattr(self.request, 'brokerage', None)
        total_received = Commission.objects.for_brokerage(brokerage).filter(
            commission_type=Commission.CommissionType.RECEIVED,
            status=Commission.Status.PAID,
        ).aggregate(total=Sum('amount'))['total'] or 0
        total_passed = Commission.objects.for_brokerage(brokerage).filter(
            commission_type=Commission.CommissionType.PASSED,
            status=Commission.Status.PAID,
        ).aggregate(total=Sum('amount'))['total'] or 0
        context['total_received'] = total_received
        context['total_passed'] = total_passed
        context['balance'] = total_received - total_passed
        return context
