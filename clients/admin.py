from django.contrib import admin

from base.admin import TenantAdminMixin, TenantFilter

from .models import Client


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'person_type', 'document', 'email', 'phone', 'city', 'state', 'is_active')
    list_filter = (TenantFilter, 'person_type', 'is_active')
    search_fields = ('name', 'document', 'email', 'phone', 'city')
