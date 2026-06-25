from django.contrib import admin

from base.admin import TenantAdminMixin

from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('original_filename', 'brokerage', 'content_type', 'object_id', 'file_size', 'uploaded_by', 'created_at')
    list_filter = ('brokerage', 'content_type')
    search_fields = ('original_filename',)
    readonly_fields = ('file_size', 'mime_type', 'original_filename', 'uploaded_by')
