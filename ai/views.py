import html
import json
import re

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, ListView

from base.mixins import TenantQuerysetMixin

from .langchain_config import get_llm
from .models import ChatMessage, ChatSession, Notification
from .tasks import summarize_client_task, summarize_policy_task, summarize_proposal_task


def format_markdown(text):
    safe = html.escape(text)
    lines = safe.split('\n')
    html_parts = []
    in_code = False
    code_buffer = []

    for line in lines:
        if line.startswith('```'):
            if in_code:
                html_parts.append(f'<pre class="bg-[#0B0F19] rounded-lg p-3 text-xs text-gray-300 overflow-x-auto"><code>{"".join(code_buffer)}</code></pre>')
                code_buffer = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_buffer.append(line + '\n')
            continue

        if not line.strip():
            html_parts.append('<br>')
            continue

        content = line.lstrip()

        if re.match(r'^#{1,3}\s', content):
            level = len(content.split(' ')[0])
            text = content[level + 1:]
            html_parts.append(f'<h{level} class="text-{"base" if level > 2 else "lg"} font-dot text-white mt-4 mb-2">{text}</h{level}>')
        elif content.startswith('- '):
            html_parts.append(f'<li class="text-xs text-gray-300 ml-4">{content[2:]}</li>')
        elif re.match(r'^\d+\.\s', content):
            html_parts.append(f'<li class="text-xs text-gray-300 ml-4">{content.split(". ", 1)[1]}</li>')
        else:
            text = content
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            text = re.sub(r'`(.+?)`', r'<code class="bg-[#0B0F19] px-1 rounded text-xs">\1</code>', text)
            html_parts.append(f'<p class="text-xs text-gray-300 leading-relaxed">{text}</p>')

    return ''.join(html_parts)


class ChatSessionListView(LoginRequiredMixin, TenantQuerysetMixin, ListView):
    context_object_name = 'sessions'
    model = ChatSession
    paginate_by = 30
    template_name = 'ai/chat_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ChatSessionDetailView(LoginRequiredMixin, View):
    template_name = 'ai/chat_detail.html'

    def get(self, request, pk):
        session = get_object_or_404(ChatSession.objects.for_request(request), pk=pk, user=request.user)
        messages_list = session.messages.all()
        return render(request, self.template_name, {'session': session, 'messages': messages_list})


class ChatSessionCreateView(LoginRequiredMixin, View):
    def post(self, request):
        session = ChatSession.objects.create(
            brokerage=request.brokerage,
            user=request.user,
            title='Nova conversa',
        )
        return redirect('chat_detail', pk=session.pk)


class ChatSessionDeleteView(LoginRequiredMixin, TenantQuerysetMixin, DeleteView):
    model = ChatSession
    success_url = reverse_lazy('chat_list')
    template_name = 'ai/chat_confirm_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ChatSendMessageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        session = get_object_or_404(ChatSession.objects.for_request(request), pk=pk, user=request.user)
        content = request.POST.get('content', '').strip()

        if not content:
            messages.error(request, 'Mensagem vazia.')
            return redirect('chat_detail', pk=pk)

        user_msg = ChatMessage.objects.create(session=session, role='user', content=content)

        if session.title == 'Nova conversa':
            session.title = content[:80]
            session.save(update_fields=['title'])

        history = list(session.messages.values_list('role', 'content'))
        llm = get_llm()

        if llm:
            try:
                prompt_parts = []
                for role, msg in history:
                    prefix = 'Usuario: ' if role == 'user' else 'Assistente: '
                    prompt_parts.append(f'{prefix}{msg}')

                system_prompt = 'Voce e um assistente de IA para uma corretora de seguros. Responda em portugues brasileiro de forma clara e concisa. Use Markdown para formatar sua resposta.'
                full_prompt = f'{system_prompt}\n\n' + '\n'.join(prompt_parts) + '\nAssistente: '
                result = llm.invoke(full_prompt)
                reply = result.content if hasattr(result, 'content') else str(result)
            except Exception:
                reply = 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.'
        else:
            reply = f'Ola! Esta e uma resposta simulada sem chave de API configurada.\n\nVoce disse: "{content[:100]}"\n\nPara ativar o chat com IA real, configure a variavel `OPENAI_API_KEY` no arquivo `.env`.'

        ChatMessage.objects.create(session=session, role='assistant', content=reply)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'user_message': content,
                'assistant_message': format_markdown(reply),
                'session_title': session.title,
            })

        return redirect('chat_detail', pk=pk)


class ChatStreamView(LoginRequiredMixin, View):
    def get(self, request, pk):
        session = get_object_or_404(ChatSession.objects.for_request(request), pk=pk, user=request.user)

        def event_stream():
            messages_list = session.messages.all()
            for msg in messages_list:
                formatted = format_markdown(msg.content)
                yield f'data: {json.dumps({"role": msg.role, "html": formatted, "content": msg.content})}\n\n'

            yield 'data: {"done": true}\n\n'

        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


class TriggerSummarizationView(LoginRequiredMixin, View):
    def post(self, request):
        content_type_id = request.POST.get('content_type')
        object_id = request.POST.get('object_id')

        if not content_type_id or not object_id:
            messages.error(request, 'Parametros invalidos.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        ct = get_object_or_404(ContentType, pk=content_type_id)
        model_class = ct.model_class()
        obj = get_object_or_404(model_class.objects.for_request(request), pk=object_id)

        task_map = {
            'client': summarize_client_task,
            'proposal': summarize_proposal_task,
            'policy': summarize_policy_task,
        }
        task_func = task_map.get(ct.model)

        if not task_func:
            messages.error(request, 'Tipo de entidade nao suportado para resumo.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        task_func.delay(object_id, request.user.pk, request.brokerage.pk)
        messages.success(request, 'Resumo com IA foi iniciado. Voce recebera uma notificacao quando ficar pronto.')
        return redirect(request.META.get('HTTP_REFERER', '/'))


class NotificationListView(LoginRequiredMixin, TenantQuerysetMixin, ListView):
    context_object_name = 'notifications'
    model = Notification
    paginate_by = 30
    template_name = 'ai/notification_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user) | qs.filter(user__isnull=True)
        return qs.distinct()


class NotificationReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, brokerage=request.brokerage)
        notification.is_read = True
        notification.save(update_fields=['is_read'])

        if notification.link:
            return redirect(notification.link)

        return redirect('notification_list')
