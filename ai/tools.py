from langchain.tools import tool

from clients.models import Client
from policies.models import Policy, Proposal


def summarize_text(entity_type, data):
    llm = None

    try:
        from .langchain_config import get_llm
        llm = get_llm()
    except ImportError:
        llm = None

    if llm:
        prompt = f'Resuma em portugues brasileiro (max 5 frases) os dados seguintes de {entity_type}:\\n\\n{data}'
        result = llm.invoke(prompt)
        return result.content if hasattr(result, 'content') else str(result)

    return f'[Simulacao] Resumo de {entity_type} gerado. Os dados foram recebidos e processados com sucesso.'


@tool
def summarize_client(client_id):
    """Resume os dados de um cliente."""
    try:
        client = Client.objects.get(pk=client_id)
        data = f'Nome: {client.name}, Documento: {client.document}, Email: {client.email}, Telefone: {client.phone}, Cidade: {client.city}/{client.state}'
        return summarize_text('cliente', data)
    except Client.DoesNotExist:
        return 'Cliente nao encontrado.'


@tool
def summarize_proposal(proposal_id):
    """Resume os dados de uma proposta."""
    try:
        proposal = Proposal.objects.select_related('client', 'branch').get(pk=proposal_id)
        data = f'Proposta: {proposal.proposal_number}, Cliente: {proposal.client}, Ramo: {proposal.branch}, Status: {proposal.status}, Valor Premio: {proposal.premium_value}, Vigencia: {proposal.start_date} a {proposal.end_date}'
        return summarize_text('proposta', data)
    except Proposal.DoesNotExist:
        return 'Proposta nao encontrada.'


@tool
def summarize_policy(policy_id):
    """Resume os dados de uma apolice."""
    try:
        policy = Policy.objects.select_related('client', 'branch').get(pk=policy_id)
        data = f'Apolice: {policy.policy_number}, Cliente: {policy.client}, Ramo: {policy.branch}, Status: {policy.status}, Valor Premio: {policy.premium_value}, Vigencia: {policy.start_date} a {policy.end_date}'
        return summarize_text('apolice', data)
    except Policy.DoesNotExist:
        return 'Apolice nao encontrada.'
