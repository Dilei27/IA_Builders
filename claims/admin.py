from django.contrib import admin

from base.admin import TenantAdminMixin

from .models import Claim


@admin.register(Claim)
class ClaimAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('claim_number', 'policy', 'covered_item', 'brokerage', 'status', 'amount_requested', 'amount_settled', 'is_active')
    list_filter = ('brokerage', 'status', 'is_active')
    search_fields = ('claim_number', 'policy__policy_number', 'covered_item__name')
