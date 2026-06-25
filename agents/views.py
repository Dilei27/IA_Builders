from django.urls import reverse_lazy

from insurers.views import CatalogCreateView, CatalogDeleteView, CatalogDetailView, CatalogUpdateView, SearchableTenantListView

from .forms import AgentForm, ProducerForm
from .models import Agent, Producer


class AgentListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Agentes',
        'title': 'Agentes',
        'subtitle': 'Agentes e assessorias parceiras da corretora.',
        'create_url_name': 'agent_create',
        'detail_url_name': 'agent_detail',
    }
    context_object_name = 'objects'
    model = Agent


class AgentDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'Agente',
        'title': 'Detalhe do agente',
        'update_url_name': 'agent_update',
        'delete_url_name': 'agent_delete',
    }
    context_object_name = 'object'
    model = Agent

    def get_details(self):
        a = self.object
        return (
            ('Documento', a.document or '-'),
            ('Email', a.email or '-'),
            ('Telefone', a.phone or '-'),
            ('Taxa de Comissão', f'{a.commission_rate:.2f}%'),
            ('Observações', a.notes or 'Sem observações.'),
            ('Status', 'Ativo' if a.is_active else 'Inativo'),
        )


class AgentCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Agentes', 'title': 'Novo agente', 'list_url_name': 'agent_list'}
    form_class = AgentForm
    model = Agent


class AgentUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Agentes', 'title': 'Editar agente', 'list_url_name': 'agent_list'}
    form_class = AgentForm
    model = Agent


class AgentDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Agentes', 'title': 'Excluir agente'}
    model = Agent
    success_url = reverse_lazy('agent_list')


class ProducerListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'Produtores',
        'title': 'Produtores',
        'subtitle': 'Corretores vinculados ou não a agentes.',
        'create_url_name': 'producer_create',
        'detail_url_name': 'producer_detail',
    }
    context_object_name = 'objects'
    model = Producer


class ProducerDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'Produtor',
        'title': 'Detalhe do produtor',
        'update_url_name': 'producer_update',
        'delete_url_name': 'producer_delete',
    }
    context_object_name = 'object'
    model = Producer

    def get_details(self):
        p = self.object
        return (
            ('Agente', p.agent or 'Sem vínculo'),
            ('Documento', p.document or '-'),
            ('Email', p.email or '-'),
            ('Telefone', p.phone or '-'),
            ('Taxa de Comissão', f'{p.commission_rate:.2f}%'),
            ('Observações', p.notes or 'Sem observações.'),
            ('Status', 'Ativo' if p.is_active else 'Inativo'),
        )


class ProducerCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'Produtores', 'title': 'Novo produtor', 'list_url_name': 'producer_list'}
    form_class = ProducerForm
    model = Producer


class ProducerUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'Produtores', 'title': 'Editar produtor', 'list_url_name': 'producer_list'}
    form_class = ProducerForm
    model = Producer


class ProducerDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'Produtores', 'title': 'Excluir produtor'}
    model = Producer
    success_url = reverse_lazy('producer_list')
