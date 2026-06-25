from django.conf import settings
from django.db import models
from django.urls import reverse

from base.managers import TenantManager
from base.models import BaseModel, BaseTenantModel


class Notification(BaseModel):
    brokerage = models.ForeignKey('core.Brokerage', on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', blank=True, null=True)
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255, blank=True)

    objects = TenantManager()

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=('brokerage', 'is_read')),
            models.Index(fields=('user', 'is_read')),
        ]

    def __str__(self):
        return self.title


class ChatSession(BaseTenantModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [models.Index(fields=('brokerage', 'user'))]

    def __str__(self):
        return self.title or f'Chat #{self.pk}'


class ChatMessage(BaseModel):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=[('user', 'Usuário'), ('assistant', 'Assistente')])
    content = models.TextField()

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'[{self.role}] {self.content[:60]}'
