from django.db import models
from django.urls import reverse

from base.models import BaseTenantModel


class Agent(BaseTenantModel):
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        indexes = [models.Index(fields=('brokerage', 'name'))]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('agent_detail', kwargs={'pk': self.pk})


class Producer(BaseTenantModel):
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, related_name='producers', blank=True, null=True)
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        indexes = [models.Index(fields=('brokerage', 'name'))]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('producer_detail', kwargs={'pk': self.pk})
