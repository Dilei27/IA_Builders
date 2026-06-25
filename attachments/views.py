import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView

from .forms import UploadForm
from .models import Attachment


class AttachmentUploadView(LoginRequiredMixin, CreateView):
    form_class = UploadForm
    model = Attachment
    template_name = 'attachments/upload.html'

    def get_initial(self):
        initial = super().get_initial()
        ct = self.request.GET.get('content_type')

        if ct:
            initial['content_type'] = ct

        object_id = self.request.GET.get('object_id')

        if object_id:
            initial['object_id'] = object_id

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('content_type'):
            try:
                ct = ContentType.objects.get_for_id(int(self.request.GET['content_type']))
                context['parent'] = ct.get_object_for_this_type(pk=self.request.GET.get('object_id'))
            except (ContentType.DoesNotExist, AttributeError, ValueError):
                pass

        return context

    def form_valid(self, form):
        if self.request.brokerage is None:
            raise PermissionDenied('User has no brokerage.')

        form.instance.brokerage = self.request.brokerage
        form.instance.original_filename = form.instance.file.name
        form.instance.file_size = form.instance.file.size
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        attachment = self.object
        obj = attachment.content_object

        if obj and hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url()

        return '/attachments/'


class AttachmentDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        attachment = get_object_or_404(Attachment.objects.for_request(request), pk=pk)

        if not os.path.exists(attachment.file.path):
            raise Http404('Arquivo não encontrado.')

        response = FileResponse(
            attachment.file.open('rb'),
            content_type=attachment.mime_type or 'application/octet-stream',
            as_attachment=True,
            filename=attachment.original_filename,
        )
        return response


class AttachmentListView(LoginRequiredMixin, View):
    def get(self, request):
        attachments = Attachment.objects.for_request(request).select_related('content_type', 'uploaded_by')
        return render(request, 'attachments/list.html', {'attachments': attachments})
