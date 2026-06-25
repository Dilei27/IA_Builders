from django.db import models
from django.db.models import Q
from django.urls import reverse

from base.models import BaseTenantModel


class Client(BaseTenantModel):
    class PersonType(models.TextChoices):
        INDIVIDUAL = 'individual', 'Pessoa Física'
        COMPANY = 'company', 'Pessoa Jurídica'

    person_type = models.CharField(max_length=20, choices=PersonType.choices, default=PersonType.INDIVIDUAL)
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address_line = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=('brokerage', 'name')),
            models.Index(fields=('brokerage', 'document')),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=('brokerage', 'document'),
                condition=~Q(document=''),
                name='unique_client_document_per_brokerage',
            ),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('client_detail', kwargs={'pk': self.pk})

# Create your models here.
