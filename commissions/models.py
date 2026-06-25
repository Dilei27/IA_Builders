from django.db import models
from django.urls import reverse

from base.models import BaseTenantModel
from policies.models import Policy


class Commission(BaseTenantModel):
    class CommissionType(models.TextChoices):
        RECEIVED = 'received', 'Recebida'
        PASSED = 'passed', 'Repassada'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente'
        PAID = 'paid', 'Paga'
        CANCELLED = 'cancelled', 'Cancelada'

    policy = models.ForeignKey(Policy, on_delete=models.PROTECT, related_name='commissions')
    commission_type = models.CharField(max_length=20, choices=CommissionType.choices, default=CommissionType.RECEIVED)
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    commission_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-commission_date', '-created_at')
        indexes = [
            models.Index(fields=('brokerage', 'commission_type')),
            models.Index(fields=('brokerage', 'status')),
            models.Index(fields=('brokerage', 'policy')),
        ]

    def __str__(self):
        return f'{self.get_commission_type_display()} - R$ {self.amount:.2f}'

    def get_absolute_url(self):
        return reverse('commission_detail', kwargs={'pk': self.pk})
