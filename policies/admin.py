from django.contrib import admin

from base.admin import TenantAdminMixin

from .models import CoveredItem, Endorsement, Policy, Proposal


@admin.register(CoveredItem)
class CoveredItemAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'client', 'branch', 'brokerage', 'item_type', 'identifier', 'is_active')
    list_filter = ('brokerage', 'branch', 'item_type', 'is_active')
    search_fields = ('name', 'identifier', 'client__name')


@admin.register(Proposal)
class ProposalAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('proposal_number', 'client', 'branch', 'brokerage', 'status', 'premium_value', 'is_active')
    list_filter = ('brokerage', 'status', 'branch', 'is_active')
    search_fields = ('proposal_number', 'client__name')
    filter_horizontal = ('coverages', 'covered_items')


@admin.register(Endorsement)
class EndorsementAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('endorsement_number', 'policy', 'brokerage', 'endorsement_type', 'effective_date', 'is_active')
    list_filter = ('brokerage', 'endorsement_type', 'is_active')
    search_fields = ('endorsement_number', 'policy__policy_number')
