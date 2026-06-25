import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views import View

from agents.models import Agent, Producer
from clients.models import Client
from crm.models import Deal
from insurers.models import Insurer
from policies.models import Policy, Proposal


class ReportPseudoBuffer:
    def write(self, value):
        return value


def csv_iterator(columns, rows):
    pseudo = ReportPseudoBuffer()
    writer = csv.writer(pseudo)
    yield writer.writerow(columns)

    for row in rows:
        yield writer.writerow(row)


class ReportsListView(LoginRequiredMixin, View):
    template_name = 'reports/list.html'

    def get(self, request):
        reports = [
            {'name': 'Clientes', 'slug': 'clients', 'description': 'Todos os clientes da corretora.', 'url_name': 'report_csv_clients'},
            {'name': 'Seguradoras', 'slug': 'insurers', 'description': 'Seguradoras cadastradas.', 'url_name': 'report_csv_insurers'},
            {'name': 'Propostas', 'slug': 'proposals', 'description': 'Propostas de seguro.', 'url_name': 'report_csv_proposals'},
            {'name': 'Apólices', 'slug': 'policies', 'description': 'Apólices ativas, canceladas e expiradas.', 'url_name': 'report_csv_policies'},
            {'name': 'Agentes', 'slug': 'agents', 'description': 'Agentes e assessorias parceiras.', 'url_name': 'report_csv_agents'},
            {'name': 'Produtores', 'slug': 'producers', 'description': 'Produtores e corretores.', 'url_name': 'report_csv_producers'},
            {'name': 'Negociações (CRM)', 'slug': 'deals', 'description': 'Negociações do pipeline CRM.', 'url_name': 'report_csv_deals'},
        ]
        return render(request, self.template_name, {'reports': reports})


class CSVExportView(LoginRequiredMixin, View):
    model = None
    columns = ()
    filename = 'export.csv'

    def get_queryset(self):
        return self.model.objects.for_request(self.request)

    def get_row(self, obj):
        return tuple(getattr(obj, col, '') for col in self.columns)

    def get(self, request):
        qs = self.get_queryset()
        rows = (self.get_row(obj) for obj in qs.iterator())
        response = StreamingHttpResponse(
            csv_iterator(self.columns, rows),
            content_type='text/csv',
        )
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'
        return response


class ClientCSVView(CSVExportView):
    model = Client
    columns = ('brokerage', 'name', 'person_type', 'document', 'email', 'phone', 'city', 'state', 'is_active')
    filename = 'clientes.csv'


class InsurerCSVView(CSVExportView):
    model = Insurer
    columns = ('brokerage', 'name', 'document', 'website', 'contact_email', 'contact_phone', 'is_active')
    filename = 'seguradoras.csv'


class ProposalCSVView(CSVExportView):
    model = Proposal
    columns = ('brokerage', 'proposal_number', 'client', 'branch', 'status', 'start_date', 'end_date', 'premium_value', 'insured_value', 'is_active')
    filename = 'propostas.csv'


class PolicyCSVView(CSVExportView):
    model = Policy
    columns = ('brokerage', 'policy_number', 'client', 'branch', 'status', 'start_date', 'end_date', 'premium_value', 'insured_value', 'is_active')
    filename = 'apolices.csv'


class AgentCSVView(CSVExportView):
    model = Agent
    columns = ('brokerage', 'name', 'document', 'email', 'phone', 'commission_rate', 'is_active')
    filename = 'agentes.csv'


class ProducerCSVView(CSVExportView):
    model = Producer
    columns = ('brokerage', 'name', 'agent', 'document', 'email', 'phone', 'commission_rate', 'is_active')
    filename = 'produtores.csv'


class DealCSVView(CSVExportView):
    model = Deal
    columns = ('brokerage', 'title', 'client', 'pipeline', 'stage', 'value', 'probability', 'is_active')
    filename = 'negociacoes.csv'
