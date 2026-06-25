from django.contrib import admin

from base.admin import TenantAdminMixin

from .models import ChatMessage, ChatSession, Notification


@admin.register(Notification)
class NotificationAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'brokerage', 'user', 'is_read', 'created_at')
    list_filter = ('brokerage', 'is_read')
    search_fields = ('title',)


@admin.register(ChatSession)
class ChatSessionAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'user', 'brokerage', 'created_at', 'is_active')
    list_filter = ('brokerage', 'is_active')
    search_fields = ('title',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('content',)
