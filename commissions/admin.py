from django.contrib import admin

from base.admin import TenantAdminMixin

from .models import Commission


@admin.register(Commission)
class CommissionAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('description', 'policy', 'brokerage', 'commission_type', 'amount', 'commission_date', 'status', 'is_active')
    list_filter = ('brokerage', 'commission_type', 'status', 'is_active')
    search_fields = ('description', 'policy__policy_number')
