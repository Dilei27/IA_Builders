import mimetypes
import uuid
from pathlib import Path

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from base.models import BaseTenantModel


ALLOWED_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.xls', '.xlsx',
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg',
    '.txt', '.csv',
}


def get_attachment_path(instance, filename):
    ext = Path(filename).suffix.lower()
    unique = uuid.uuid4().hex
    ct = instance.content_type
    return f'attachments/{instance.brokerage_id}/{ct.app_label}/{ct.model}/{instance.object_id}/{unique}{ext}'


class Attachment(BaseTenantModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    file = models.FileField(upload_to=get_attachment_path)
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=127, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_attachments',
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=('brokerage', 'content_type', 'object_id')),
        ]

    def __str__(self):
        return self.original_filename

    def get_absolute_url(self):
        return reverse('attachment_download', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.mime_type:
            guessed, _ = mimetypes.guess_type(self.original_filename)
            self.mime_type = guessed or 'application/octet-stream'

        if not self.file_size and self.file:
            try:
                self.file_size = self.file.size
            except (OSError, AttributeError):
                pass

        super().save(*args, **kwargs)
