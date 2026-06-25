from django.db import models
from django.urls import reverse

from base.models import BaseTenantModel
from clients.models import Client


class Pipeline(BaseTenantModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        indexes = [models.Index(fields=('brokerage', 'name'))]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pipeline_detail', kwargs={'pk': self.pk})


class PipelineStage(BaseTenantModel):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=7, default='#3B82F6')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('pipeline', 'order', 'name')
        indexes = [models.Index(fields=('brokerage', 'pipeline'))]

    def __str__(self):
        return f'{self.pipeline} - {self.name}'

    def get_absolute_url(self):
        return reverse('pipelinestage_detail', kwargs={'pk': self.pk})


class Deal(BaseTenantModel):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.PROTECT, related_name='deals')
    stage = models.ForeignKey(PipelineStage, on_delete=models.PROTECT, related_name='deals')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='deals')
    title = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    probability = models.PositiveIntegerField(default=50)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=('brokerage', 'pipeline')),
            models.Index(fields=('brokerage', 'stage')),
            models.Index(fields=('brokerage', 'client')),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('deal_detail', kwargs={'pk': self.pk})
