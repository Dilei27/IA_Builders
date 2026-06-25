from django.contrib import admin

from base.admin import TenantAdminMixin

from .models import Deal, Pipeline, PipelineStage


@admin.register(Pipeline)
class PipelineAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'brokerage', 'is_active')
    list_filter = ('brokerage', 'is_active')
    search_fields = ('name',)


@admin.register(PipelineStage)
class PipelineStageAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'pipeline', 'brokerage', 'order', 'color', 'is_active')
    list_filter = ('brokerage', 'pipeline', 'is_active')
    search_fields = ('name',)


@admin.register(Deal)
class DealAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'client', 'pipeline', 'stage', 'brokerage', 'value', 'probability', 'is_active')
    list_filter = ('brokerage', 'pipeline', 'stage', 'is_active')
    search_fields = ('title', 'client__name')
