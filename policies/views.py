from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.mixins import TenantQuerysetMixin
from insurers.views import CatalogCreateView, CatalogDeleteView, CatalogDetailView, CatalogUpdateView, SearchableTenantListView

from .forms import CoveredItemForm, EndorsementForm, PolicyForm, ProposalForm
from .models import CoveredItem, Endorsement, Policy, Proposal


class CoveredItemListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Itens Cobertos',
        'title': 'Itens cobertos',
        'subtitle': 'Objetos segurados vinculados a clientes e ramos.',
        'create_url_name': 'covered_item_create',
        'detail_url_name': 'covered_item_detail',
    }
    context_object_name = 'objects'
    model = CoveredItem


class CoveredItemDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'Item coberto',
        'title': 'Detalhe do item coberto',
        'update_url_name': 'covered_item_update',
        'delete_url_name': 'covered_item_delete',
    }
    context_object_name = 'object'
    model = CoveredItem

    def get_details(self):
        item = self.object
        return (
            ('Cliente', item.client),
            ('Ramo', item.branch),
            ('Tipo', item.get_item_type_display()),
            ('Identificador', item.identifier or '-'),
            ('Status', 'Ativo' if item.is_active else 'Inativo'),
            ('Descrição', item.description or 'Sem descrição.'),
        )


class CoveredItemCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Itens Cobertos', 'title': 'Novo item coberto', 'list_url_name': 'covered_item_list'}
    form_class = CoveredItemForm
    model = CoveredItem


class CoveredItemUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Itens Cobertos', 'title': 'Editar item coberto', 'list_url_name': 'covered_item_list'}
    form_class = CoveredItemForm
    model = CoveredItem


class CoveredItemDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Itens Cobertos', 'title': 'Excluir item coberto'}
    model = CoveredItem
    success_url = reverse_lazy('covered_item_list')


class ProposalListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Propostas',
        'title': 'Propostas',
        'subtitle': 'Propostas de seguros por corretora.',
        'create_url_name': 'proposal_create',
        'detail_url_name': 'proposal_detail',
    }
    context_object_name = 'objects'
    model = Proposal

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')

        if status:
            qs = qs.filter(status=status)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_generate'] = True
        return context


class ProposalDetailView(LoginRequiredMixin, TenantQuerysetMixin, DetailView):
    context_object_name = 'object'
    model = Proposal
    template_name = 'policies/proposal_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposal = self.object
        context['coverages_list'] = proposal.coverages.all()
        context['covered_items_list'] = proposal.covered_items.all()
        context['can_generate_policy'] = proposal.status != Proposal.Status.CONVERTED
        return context


class ProposalCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Propostas', 'title': 'Nova proposta', 'list_url_name': 'proposal_list'}
    form_class = ProposalForm
    model = Proposal


class ProposalUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Propostas', 'title': 'Editar proposta', 'list_url_name': 'proposal_list'}
    form_class = ProposalForm
    model = Proposal


class ProposalDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Propostas', 'title': 'Excluir proposta'}
    model = Proposal
    success_url = reverse_lazy('proposal_list')


class GeneratePolicyView(LoginRequiredMixin, View):
    def post(self, request, pk):
        proposal = get_object_or_404(Proposal.objects.for_request(request), pk=pk)

        if proposal.status == Proposal.Status.CONVERTED:
            messages.warning(request, 'Esta proposta já foi convertida em apólice.')
            return redirect(proposal)

        policy = Policy(
            brokerage=proposal.brokerage,
            proposal=proposal,
            client=proposal.client,
            branch=proposal.branch,
            insurer=proposal.insurer,
            policy_number=f'POL-{proposal.proposal_number or proposal.pk}',
            status=Policy.Status.ACTIVE,
            start_date=proposal.start_date,
            end_date=proposal.end_date,
            premium_value=proposal.premium_value,
            insured_value=proposal.insured_value,
            notes=proposal.notes,
        )
        policy.save()
        policy.coverages.set(proposal.coverages.all())
        policy.covered_items.set(proposal.covered_items.all())

        proposal.status = Proposal.Status.CONVERTED
        proposal.save()

        messages.success(request, 'Apólice gerada com sucesso a partir da proposta.')
        return redirect(policy)


class PolicyListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Apólices',
        'title': 'Apólices',
        'subtitle': 'Apólices ativas, canceladas e expiradas por corretora.',
        'create_url_name': 'policy_create',
        'detail_url_name': 'policy_detail',
    }
    context_object_name = 'objects'
    model = Policy

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')

        if status:
            qs = qs.filter(status=status)

        return qs


class PolicyDetailView(LoginRequiredMixin, TenantQuerysetMixin, DetailView):
    context_object_name = 'object'
    model = Policy
    template_name = 'policies/policy_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        policy = self.object
        context['coverages_list'] = policy.coverages.all()
        context['covered_items_list'] = policy.covered_items.all()
        return context


class PolicyCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Apólices', 'title': 'Nova apólice', 'list_url_name': 'policy_list'}
    form_class = PolicyForm
    model = Policy


class PolicyUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Apólices', 'title': 'Editar apólice', 'list_url_name': 'policy_list'}
    form_class = PolicyForm
    model = Policy


class PolicyDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Apólices', 'title': 'Excluir apólice'}
    model = Policy
    success_url = reverse_lazy('policy_list')


class EndorsementListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Endossos',
        'title': 'Endossos',
        'subtitle': 'Endossos vinculados a apólices.',
        'create_url_name': 'endorsement_create',
        'detail_url_name': 'endorsement_detail',
    }
    context_object_name = 'objects'
    model = Endorsement


class EndorsementDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'Endosso',
        'title': 'Detalhe do endosso',
        'update_url_name': 'endorsement_update',
        'delete_url_name': 'endorsement_delete',
    }
    context_object_name = 'object'
    model = Endorsement

    def get_details(self):
        e = self.object
        return (
            ('Nº Endosso', e.endorsement_number or '-'),
            ('Tipo', e.get_endorsement_type_display()),
            ('Apólice', e.policy),
            ('Data Efetiva', e.effective_date.strftime('%d/%m/%Y') if e.effective_date else '-'),
            ('Descrição', e.description or 'Sem descrição.'),
            ('Observações', e.notes or 'Sem observações.'),
        )


class EndorsementCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Endossos', 'title': 'Novo endosso', 'list_url_name': 'endorsement_list'}
    form_class = EndorsementForm
    model = Endorsement


class EndorsementUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Endossos', 'title': 'Editar endosso', 'list_url_name': 'endorsement_list'}
    form_class = EndorsementForm
    model = Endorsement


class EndorsementDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Endossos', 'title': 'Excluir endosso'}
    model = Endorsement
    success_url = reverse_lazy('endorsement_list')
