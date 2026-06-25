from django.db import models
from django.urls import reverse

from base.models import BaseTenantModel
from policies.models import CoveredItem, Policy


class Claim(BaseTenantModel):
    class Status(models.TextChoices):
        OPEN = 'open', 'Aberto'
        IN_PROGRESS = 'in_progress', 'Em Andamento'
        SETTLED = 'settled', 'Liquidado'
        REJECTED = 'rejected', 'Recusado'

    policy = models.ForeignKey(Policy, on_delete=models.PROTECT, related_name='claims')
    covered_item = models.ForeignKey(CoveredItem, on_delete=models.PROTECT, related_name='claims')
    claim_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    occurrence_date = models.DateField(blank=True, null=True)
    notification_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    amount_requested = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    amount_settled = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=('brokerage', 'status')),
            models.Index(fields=('brokerage', 'policy')),
        ]

    def __str__(self):
        return self.claim_number or f'Sinistro #{self.pk}'

    def get_absolute_url(self):
        return reverse('claim_detail', kwargs={'pk': self.pk})
