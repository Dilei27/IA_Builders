from django.urls import path

from .views import (
    AgentCreateView,
    AgentDeleteView,
    AgentDetailView,
    AgentListView,
    AgentUpdateView,
    ProducerCreateView,
    ProducerDeleteView,
    ProducerDetailView,
    ProducerListView,
    ProducerUpdateView,
)


urlpatterns = [
    path('agents/', AgentListView.as_view(), name='agent_list'),
    path('agents/create/', AgentCreateView.as_view(), name='agent_create'),
    path('agents/<int:pk>/', AgentDetailView.as_view(), name='agent_detail'),
    path('agents/<int:pk>/edit/', AgentUpdateView.as_view(), name='agent_update'),
    path('agents/<int:pk>/delete/', AgentDeleteView.as_view(), name='agent_delete'),
    path('producers/', ProducerListView.as_view(), name='producer_list'),
    path('producers/create/', ProducerCreateView.as_view(), name='producer_create'),
    path('producers/<int:pk>/', ProducerDetailView.as_view(), name='producer_detail'),
    path('producers/<int:pk>/edit/', ProducerUpdateView.as_view(), name='producer_update'),
    path('producers/<int:pk>/delete/', ProducerDeleteView.as_view(), name='producer_delete'),
]
