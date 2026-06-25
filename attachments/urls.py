from django.urls import path

from .views import AttachmentDownloadView, AttachmentListView, AttachmentUploadView


urlpatterns = [
    path('attachments/', AttachmentListView.as_view(), name='attachment_list'),
    path('attachments/upload/', AttachmentUploadView.as_view(), name='attachment_upload'),
    path('attachments/<int:pk>/download/', AttachmentDownloadView.as_view(), name='attachment_download'),
]
