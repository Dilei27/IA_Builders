from django.urls import path

from .views import (
    ChatSendMessageView,
    ChatSessionCreateView,
    ChatSessionDeleteView,
    ChatSessionDetailView,
    ChatSessionListView,
    ChatStreamView,
    NotificationListView,
    NotificationReadView,
    TriggerSummarizationView,
)


urlpatterns = [
    path('ai/summarize/', TriggerSummarizationView.as_view(), name='ai_summarize'),
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/read/', NotificationReadView.as_view(), name='notification_read'),
    path('chat/', ChatSessionListView.as_view(), name='chat_list'),
    path('chat/new/', ChatSessionCreateView.as_view(), name='chat_new'),
    path('chat/<int:pk>/', ChatSessionDetailView.as_view(), name='chat_detail'),
    path('chat/<int:pk>/send/', ChatSendMessageView.as_view(), name='chat_send'),
    path('chat/<int:pk>/delete/', ChatSessionDeleteView.as_view(), name='chat_delete'),
    path('chat/<int:pk>/stream/', ChatStreamView.as_view(), name='chat_stream'),
]
