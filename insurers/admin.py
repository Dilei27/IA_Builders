from django.contrib import admin

from base.admin import TenantAdminMixin

from .models import Branch, Coverage, Insurer


@admin.register(Insurer)
class InsurerAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'brokerage', 'document', 'contact_email', 'contact_phone', 'is_active')
    list_filter = ('brokerage', 'is_active')
    search_fields = ('name', 'document', 'contact_email', 'contact_phone')


@admin.register(Branch)
class BranchAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'brokerage', 'is_active')
    list_filter = ('brokerage', 'is_active')
    search_fields = ('name',)


@admin.register(Coverage)
class CoverageAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'branch', 'brokerage', 'is_active')
    list_filter = ('brokerage', 'branch', 'is_active')
    search_fields = ('name', 'branch__name')
