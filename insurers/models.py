from django.db import models
from django.urls import reverse

from base.models import BaseTenantModel


class Insurer(BaseTenantModel):
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=('brokerage', 'name')),
            models.Index(fields=('brokerage', 'document')),
        ]
        constraints = [
            models.UniqueConstraint(fields=('brokerage', 'name'), name='unique_insurer_name_per_brokerage'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('insurer_detail', kwargs={'pk': self.pk})


class Branch(BaseTenantModel):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        indexes = [models.Index(fields=('brokerage', 'name'))]
        constraints = [
            models.UniqueConstraint(fields=('brokerage', 'name'), name='unique_branch_name_per_brokerage'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('branch_detail', kwargs={'pk': self.pk})


class Coverage(BaseTenantModel):
    name = models.CharField(max_length=160)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='coverages')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('branch__name', 'name')
        indexes = [models.Index(fields=('brokerage', 'name'))]
        constraints = [
            models.UniqueConstraint(fields=('brokerage', 'branch', 'name'), name='unique_coverage_name_per_branch'),
        ]

    def __str__(self):
        return f'{self.branch} - {self.name}'

    def get_absolute_url(self):
        return reverse('coverage_detail', kwargs={'pk': self.pk})

# Create your models here.
