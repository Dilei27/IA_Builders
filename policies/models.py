from django.db import models
from django.urls import reverse

from base.models import BaseTenantModel
from clients.models import Client
from insurers.models import Branch, Coverage, Insurer


class CoveredItem(BaseTenantModel):
    class ItemType(models.TextChoices):
        VEHICLE = 'vehicle', 'Automóvel'
        PROPERTY = 'property', 'Imóvel'
        FLEET = 'fleet', 'Frota'
        TRAVEL = 'travel', 'Viagem'
        LIFE = 'life', 'Vida'
        OTHER = 'other', 'Outro'

    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='covered_items')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='covered_items')
    item_type = models.CharField(max_length=20, choices=ItemType.choices, default=ItemType.OTHER)
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=('brokerage', 'name')),
            models.Index(fields=('brokerage', 'identifier')),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('covered_item_detail', kwargs={'pk': self.pk})


class Proposal(BaseTenantModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Rascunho'
        SENT = 'sent', 'Enviada'
        APPROVED = 'approved', 'Aprovada'
        REJECTED = 'rejected', 'Recusada'
        CONVERTED = 'converted', 'Convertida em Apólice'

    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='proposals')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='proposals')
    insurer = models.ForeignKey(Insurer, on_delete=models.PROTECT, related_name='proposals', blank=True, null=True)
    coverages = models.ManyToManyField(Coverage, related_name='proposals', blank=True)
    covered_items = models.ManyToManyField(CoveredItem, related_name='proposals', blank=True)
    proposal_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    premium_value = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    insured_value = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=('brokerage', 'status')),
            models.Index(fields=('brokerage', 'client')),
        ]
        constraints = [
            models.UniqueConstraint(fields=('brokerage', 'proposal_number'), condition=~models.Q(proposal_number=''), name='unique_proposal_number_per_brokerage'),
        ]

    def __str__(self):
        return self.proposal_number or f'Proposta #{self.pk}'

    def get_absolute_url(self):
        return reverse('proposal_detail', kwargs={'pk': self.pk})


class Policy(BaseTenantModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Ativa'
        CANCELLED = 'cancelled', 'Cancelada'
        EXPIRED = 'expired', 'Expirada'

    proposal = models.ForeignKey(Proposal, on_delete=models.SET_NULL, related_name='policies', blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='policies')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='policies')
    insurer = models.ForeignKey(Insurer, on_delete=models.PROTECT, related_name='policies', blank=True, null=True)
    coverages = models.ManyToManyField(Coverage, related_name='policies', blank=True)
    covered_items = models.ManyToManyField(CoveredItem, related_name='policies', blank=True)
    policy_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    premium_value = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    insured_value = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=('brokerage', 'status')),
            models.Index(fields=('brokerage', 'client')),
        ]
        constraints = [
            models.UniqueConstraint(fields=('brokerage', 'policy_number'), condition=~models.Q(policy_number=''), name='unique_policy_number_per_brokerage'),
        ]

    def __str__(self):
        return self.policy_number or f'Apólice #{self.pk}'

    def get_absolute_url(self):
        return reverse('policy_detail', kwargs={'pk': self.pk})


class Endorsement(BaseTenantModel):
    class EndorsementType(models.TextChoices):
        INCLUSION = 'inclusion', 'Inclusão'
        EXCLUSION = 'exclusion', 'Exclusão'
        ALTERATION = 'alteration', 'Alteração'
        CANCELLATION = 'cancellation', 'Cancelamento'

    policy = models.ForeignKey(Policy, on_delete=models.PROTECT, related_name='endorsements')
    endorsement_number = models.CharField(max_length=20, blank=True)
    endorsement_type = models.CharField(max_length=20, choices=EndorsementType.choices, default=EndorsementType.ALTERATION)
    description = models.TextField(blank=True)
    effective_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=('brokerage', 'policy')),
        ]

    def __str__(self):
        return self.endorsement_number or f'Endosso #{self.pk}'

    def get_absolute_url(self):
        return reverse('endorsement_detail', kwargs={'pk': self.pk})
