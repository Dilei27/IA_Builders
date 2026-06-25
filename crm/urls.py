from django.urls import path

from .views import (
    DealCreateView,
    DealDeleteView,
    DealDetailView,
    DealListView,
    DealUpdateView,
    KanbanMoveDealView,
    PipelineCreateView,
    PipelineDeleteView,
    PipelineDetailView,
    PipelineListView,
    PipelineStageCreateView,
    PipelineStageDeleteView,
    PipelineStageDetailView,
    PipelineStageListView,
    PipelineStageUpdateView,
    PipelineUpdateView,
)


urlpatterns = [
    path('pipelines/', PipelineListView.as_view(), name='pipeline_list'),
    path('pipelines/create/', PipelineCreateView.as_view(), name='pipeline_create'),
    path('pipelines/<int:pk>/', PipelineDetailView.as_view(), name='pipeline_detail'),
    path('pipelines/<int:pk>/edit/', PipelineUpdateView.as_view(), name='pipeline_update'),
    path('pipelines/<int:pk>/delete/', PipelineDeleteView.as_view(), name='pipeline_delete'),
    path('stages/', PipelineStageListView.as_view(), name='pipelinestage_list'),
    path('stages/create/', PipelineStageCreateView.as_view(), name='pipelinestage_create'),
    path('stages/<int:pk>/', PipelineStageDetailView.as_view(), name='pipelinestage_detail'),
    path('stages/<int:pk>/edit/', PipelineStageUpdateView.as_view(), name='pipelinestage_update'),
    path('stages/<int:pk>/delete/', PipelineStageDeleteView.as_view(), name='pipelinestage_delete'),
    path('deals/', DealListView.as_view(), name='deal_list'),
    path('deals/create/', DealCreateView.as_view(), name='deal_create'),
    path('deals/<int:pk>/', DealDetailView.as_view(), name='deal_detail'),
    path('deals/<int:pk>/edit/', DealUpdateView.as_view(), name='deal_update'),
    path('deals/<int:pk>/delete/', DealDeleteView.as_view(), name='deal_delete'),
    path('deals/<int:pk>/move/', KanbanMoveDealView.as_view(), name='deal_move'),
]
