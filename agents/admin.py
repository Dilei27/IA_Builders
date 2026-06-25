from django.contrib import admin

from base.admin import TenantAdminMixin

from .models import Agent, Producer


@admin.register(Agent)
class AgentAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'brokerage', 'document', 'email', 'phone', 'commission_rate', 'is_active')
    list_filter = ('brokerage', 'is_active')
    search_fields = ('name', 'document', 'email')


@admin.register(Producer)
class ProducerAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'agent', 'brokerage', 'document', 'email', 'commission_rate', 'is_active')
    list_filter = ('brokerage', 'agent', 'is_active')
    search_fields = ('name', 'document', 'email')
