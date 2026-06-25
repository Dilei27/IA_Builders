from django.urls import path

from .views import (
    AgentCSVView,
    ClientCSVView,
    DealCSVView,
    InsurerCSVView,
    PolicyCSVView,
    ProducerCSVView,
    ProposalCSVView,
    ReportsListView,
)


urlpatterns = [
    path('reports/', ReportsListView.as_view(), name='report_list'),
    path('reports/csv/clients/', ClientCSVView.as_view(), name='report_csv_clients'),
    path('reports/csv/insurers/', InsurerCSVView.as_view(), name='report_csv_insurers'),
    path('reports/csv/proposals/', ProposalCSVView.as_view(), name='report_csv_proposals'),
    path('reports/csv/policies/', PolicyCSVView.as_view(), name='report_csv_policies'),
    path('reports/csv/agents/', AgentCSVView.as_view(), name='report_csv_agents'),
    path('reports/csv/producers/', ProducerCSVView.as_view(), name='report_csv_producers'),
    path('reports/csv/deals/', DealCSVView.as_view(), name='report_csv_deals'),
]
