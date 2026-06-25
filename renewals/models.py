from django.db import models
from django.urls import reverse

from base.models import BaseTenantModel
from policies.models import Policy


class Renewal(BaseTenantModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente'
        RENEWED = 'renewed', 'Renovado'
        EXPIRED = 'expired', 'Expirado'

    policy = models.ForeignKey(Policy, on_delete=models.PROTECT, related_name='renewals')
    renewal_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    previous_end_date = models.DateField(blank=True, null=True)
    new_start_date = models.DateField(blank=True, null=True)
    new_end_date = models.DateField(blank=True, null=True)
    premium_value = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=('brokerage', 'status')),
            models.Index(fields=('brokerage', 'policy')),
        ]

    def __str__(self):
        return self.renewal_number or f'Renovação #{self.pk}'

    def get_absolute_url(self):
        return reverse('renewal_detail', kwargs={'pk': self.pk})
