from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.mixins import TenantQuerysetMixin
from insurers.views import CatalogCreateView, CatalogDeleteView, CatalogDetailView, CatalogUpdateView, SearchableTenantListView

from .forms import DealForm, PipelineForm, PipelineStageForm
from .models import Deal, Pipeline, PipelineStage


class PipelineListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'CRM',
        'title': 'Pipelines',
        'subtitle': 'Pipelines de vendas personalizáveis por corretora.',
        'create_url_name': 'pipeline_create',
        'detail_url_name': 'pipeline_detail',
    }
    context_object_name = 'objects'
    model = Pipeline


class PipelineDetailView(LoginRequiredMixin, TenantQuerysetMixin, DetailView):
    context_object_name = 'object'
    model = Pipeline
    template_name = 'crm/pipeline_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pipeline = self.object
        context['stages'] = pipeline.stages.filter(is_active=True).order_by('order', 'name').annotate(deal_count=Count('deals'))
        context['deals_by_stage'] = {
            stage.pk: Deal.objects.for_request(self.request).filter(stage=stage, is_active=True)
            for stage in context['stages']
        }
        return context


class PipelineCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'CRM', 'title': 'Novo pipeline', 'list_url_name': 'pipeline_list'}
    form_class = PipelineForm
    model = Pipeline


class PipelineUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'CRM', 'title': 'Editar pipeline', 'list_url_name': 'pipeline_list'}
    form_class = PipelineForm
    model = Pipeline


class PipelineDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'CRM', 'title': 'Excluir pipeline'}
    model = Pipeline
    success_url = reverse_lazy('pipeline_list')


class PipelineStageListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'CRM',
        'title': 'Etapas de pipeline',
        'subtitle': 'Etapas com nome, cor e ordem.',
        'create_url_name': 'pipelinestage_create',
        'detail_url_name': 'pipelinestage_detail',
    }
    context_object_name = 'objects'
    model = PipelineStage


class PipelineStageDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'CRM',
        'title': 'Detalhe da etapa',
        'update_url_name': 'pipelinestage_update',
        'delete_url_name': 'pipelinestage_delete',
    }
    context_object_name = 'object'
    model = PipelineStage

    def get_details(self):
        s = self.object
        return (
            ('Pipeline', s.pipeline),
            ('Nome', s.name),
            ('Ordem', s.order),
            ('Status', 'Ativo' if s.is_active else 'Inativo'),
        )


class PipelineStageCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'CRM', 'title': 'Nova etapa', 'list_url_name': 'pipelinestage_list'}
    form_class = PipelineStageForm
    model = PipelineStage


class PipelineStageUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'CRM', 'title': 'Editar etapa', 'list_url_name': 'pipelinestage_list'}
    form_class = PipelineStageForm
    model = PipelineStage


class PipelineStageDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'CRM', 'title': 'Excluir etapa'}
    model = PipelineStage
    success_url = reverse_lazy('pipelinestage_list')


class DealListView(SearchableTenantListView):
    catalog_context = {
        'section_label': 'CRM',
        'title': 'Negociações',
        'subtitle': 'Grid de negociações por corretora.',
        'create_url_name': 'deal_create',
        'detail_url_name': 'deal_detail',
    }
    context_object_name = 'objects'
    model = Deal


class DealDetailView(CatalogDetailView):
    catalog_context = {
        'section_label': 'CRM',
        'title': 'Detalhe da negociação',
        'update_url_name': 'deal_update',
        'delete_url_name': 'deal_delete',
    }
    context_object_name = 'object'
    model = Deal

    def get_details(self):
        d = self.object
        return (
            ('Pipeline', d.pipeline),
            ('Etapa', d.stage),
            ('Cliente', d.client),
            ('Valor', f'R$ {d.value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') if d.value else '-'),
            ('Probabilidade', f'{d.probability}%'),
            ('Descrição', d.description or 'Sem descrição.'),
            ('Observações', d.notes or 'Sem observações.'),
            ('Resumo IA', d.ai_summary or 'Nenhum resumo gerado.'),
        )


class DealCreateView(CatalogCreateView):
    catalog_context = {'section_label': 'CRM', 'title': 'Nova negociação', 'list_url_name': 'deal_list'}
    form_class = DealForm
    model = Deal


class DealUpdateView(CatalogUpdateView):
    catalog_context = {'section_label': 'CRM', 'title': 'Editar negociação', 'list_url_name': 'deal_list'}
    form_class = DealForm
    model = Deal


class DealDeleteView(CatalogDeleteView):
    catalog_context = {'section_label': 'CRM', 'title': 'Excluir negociação'}
    model = Deal
    success_url = reverse_lazy('deal_list')


class KanbanMoveDealView(LoginRequiredMixin, View):
    def post(self, request, pk):
        deal = get_object_or_404(Deal.objects.for_request(request), pk=pk)
        stage_pk = request.POST.get('stage')

        if stage_pk:
            stage = get_object_or_404(PipelineStage.objects.for_request(request), pk=stage_pk)
            deal.stage = stage
            deal.save()
            messages.success(request, f'Negociação movida para "{stage.name}".')

        return redirect(request.POST.get('next', deal.get_absolute_url()))
