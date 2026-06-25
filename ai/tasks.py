from celery import shared_task

from clients.models import Client
from policies.models import Policy, Proposal

from .models import Notification
from .tools import summarize_text


def create_notification(brokerage, user, title, message, link=''):
    Notification.objects.create(
        brokerage=brokerage,
        user=user,
        title=title,
        message=message,
        link=link,
    )


@shared_task
def summarize_client_task(client_id, user_id, brokerage_id):
    from django.contrib.auth import get_user_model
    from core.models import Brokerage

    User = get_user_model()

    try:
        client = Client.objects.select_related('brokerage').get(pk=client_id)
        data = f'Nome: {client.name}, Documento: {client.document}, Email: {client.email}, Telefone: {client.phone}, Cidade: {client.city}/{client.state}'
        summary = summarize_text('cliente', data)
        client.ai_summary = summary
        client.save(update_fields=['ai_summary'])
        create_notification(
            Brokerage.objects.get(pk=brokerage_id),
            User.objects.get(pk=user_id),
            'Resumo de cliente concluido',
            f'O resumo do cliente {client.name} foi gerado com sucesso.',
            client.get_absolute_url(),
        )
        return summary
    except Client.DoesNotExist:
        return None


@shared_task
def summarize_proposal_task(proposal_id, user_id, brokerage_id):
    from django.contrib.auth import get_user_model
    from core.models import Brokerage

    User = get_user_model()

    try:
        proposal = Proposal.objects.select_related('client', 'branch').get(pk=proposal_id)
        data = f'Proposta: {proposal.proposal_number}, Cliente: {proposal.client}, Ramo: {proposal.branch}, Status: {proposal.get_status_display()}, Premio: {proposal.premium_value}, Vigencia: {proposal.start_date} a {proposal.end_date}'
        summary = summarize_text('proposta', data)
        proposal.ai_summary = summary
        proposal.save(update_fields=['ai_summary'])
        create_notification(
            Brokerage.objects.get(pk=brokerage_id),
            User.objects.get(pk=user_id),
            'Resumo de proposta concluido',
            f'O resumo da proposta {proposal} foi gerado com sucesso.',
            proposal.get_absolute_url(),
        )
        return summary
    except Proposal.DoesNotExist:
        return None


@shared_task
def summarize_policy_task(policy_id, user_id, brokerage_id):
    from django.contrib.auth import get_user_model
    from core.models import Brokerage

    User = get_user_model()

    try:
        policy = Policy.objects.select_related('client', 'branch').get(pk=policy_id)
        data = f'Apolice: {policy.policy_number}, Cliente: {policy.client}, Ramo: {policy.branch}, Status: {policy.get_status_display()}, Premio: {policy.premium_value}, Vigencia: {policy.start_date} a {policy.end_date}'
        summary = summarize_text('apolice', data)
        policy.ai_summary = summary
        policy.save(update_fields=['ai_summary'])
        create_notification(
            Brokerage.objects.get(pk=brokerage_id),
            User.objects.get(pk=user_id),
            'Resumo de apolice concluido',
            f'O resumo da apolice {policy} foi gerado com sucesso.',
            policy.get_absolute_url(),
        )
        return summary
    except Policy.DoesNotExist:
        return None
