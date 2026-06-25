from django.contrib import admin

from base.admin import TenantAdminMixin

from .models import Renewal


@admin.register(Renewal)
class RenewalAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('renewal_number', 'policy', 'brokerage', 'status', 'new_start_date', 'new_end_date', 'is_active')
    list_filter = ('brokerage', 'status', 'is_active')
    search_fields = ('renewal_number', 'policy__policy_number')
