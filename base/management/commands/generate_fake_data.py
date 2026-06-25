import random
from datetime import date, timedelta

from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from agents.models import Agent, Producer
from attachments.models import Attachment
from claims.models import Claim
from clients.models import Client
from crm.models import Deal, Pipeline, PipelineStage
from insurers.models import Branch, Coverage, Insurer
from policies.models import CoveredItem, Endorsement, Policy, Proposal
from renewals.models import Renewal


class Command(BaseCommand):
    help = 'Gera dados ficticios para desenvolvimento.'

    def handle(self, *args, **options):
        from core.models import Brokerage, User

        self.stdout.write('Gerando dados ficticios...')

        Brokerage.objects.all().delete()

        br1 = Brokerage.objects.create(cnpj='11222333000181', legal_name='Corretora Seguro Total Ltda', trade_name='Seguro Total', plan='free')
        br2 = Brokerage.objects.create(cnpj='99888777000155', legal_name='Protecao Maxima Corretora Ltda', trade_name='Protecao Maxima', plan='free')

        owner1 = User.objects.create_user(email='admin@segurototal.com', password='123', brokerage=br1, full_name='Admin Seguro Total', role='owner')
        owner2 = User.objects.create_user(email='admin@protecaomaxima.com', password='123', brokerage=br2, full_name='Admin Protecao Maxima', role='owner')

        for brokerage, owner in [(br1, owner1), (br2, owner2)]:
            clients = []
            for i in range(10):
                c = Client.objects.create(
                    brokerage=brokerage,
                    person_type=random.choice(['individual', 'company']),
                    name=f'Cliente {i+1} da {brokerage}',
                    document=str(random.randint(10000000000, 99999999999)),
                    email=f'cliente{i+1}@email.com',
                    phone=f'(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}',
                    city=random.choice(['Sao Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba']),
                    state=random.choice(['SP', 'RJ', 'MG', 'PR']),
                )
                clients.append(c)

            ins1 = Insurer.objects.create(brokerage=brokerage, name='SulAmerica Seguros', document='12345678000190')
            ins2 = Insurer.objects.create(brokerage=brokerage, name='Porto Seguro', document='98765432000110')
            Insurer.objects.create(brokerage=brokerage, name='Bradesco Seguros', document='55667788000122')

            branch_auto = Branch.objects.create(brokerage=brokerage, name='Automovel')
            branch_vida = Branch.objects.create(brokerage=brokerage, name='Vida')
            branch_resid = Branch.objects.create(brokerage=brokerage, name='Residencial')

            for branch in [branch_auto, branch_vida, branch_resid]:
                for cov_name in ['Basica', 'Premium', 'VIP']:
                    Coverage.objects.create(brokerage=brokerage, branch=branch, name=f'{cov_name} - {branch.name}')

            for i in range(5):
                client = random.choice(clients)
                branch = random.choice([branch_auto, branch_vida, branch_resid])
                prop = Proposal.objects.create(
                    brokerage=brokerage,
                    client=client,
                    branch=branch,
                    insurer=random.choice([ins1, ins2]),
                    proposal_number=f'PROP-{brokerage.pk}-{i+1}',
                    status=random.choice(['draft', 'sent', 'approved', 'rejected']),
                    start_date=date.today(),
                    end_date=date.today() + timedelta(days=365),
                    premium_value=random.uniform(500, 5000),
                    insured_value=random.uniform(50000, 500000),
                )

                for j in range(random.randint(1, 3)):
                    CoveredItem.objects.create(
                        brokerage=brokerage,
                        client=client,
                        branch=branch,
                        item_type=random.choice(['vehicle', 'property', 'life']),
                        name=f'Item {j+1} - {client.name}',
                        identifier=str(random.randint(1000, 9999)),
                    )

            for i in range(3):
                client = random.choice(clients)
                branch = random.choice([branch_auto, branch_vida, branch_resid])
                pol = Policy.objects.create(
                    brokerage=brokerage,
                    client=client,
                    branch=branch,
                    insurer=random.choice([ins1, ins2]),
                    policy_number=f'POL-{brokerage.pk}-{i+1}',
                    status=random.choice(['active', 'active', 'active', 'expired']),
                    start_date=date.today(),
                    end_date=date.today() + timedelta(days=365),
                    premium_value=random.uniform(500, 5000),
                    insured_value=random.uniform(50000, 500000),
                )

                for j in range(2):
                    Claim.objects.create(
                        brokerage=brokerage,
                        policy=pol,
                        covered_item=CoveredItem.objects.filter(brokerage=brokerage).first(),
                        claim_number=f'CL-{brokerage.pk}-{i+1}-{j+1}',
                        status=random.choice(['open', 'in_progress', 'settled']),
                        occurrence_date=date.today() - timedelta(days=random.randint(1, 60)),
                        amount_requested=random.uniform(1000, 50000),
                    )

                Renewal.objects.create(
                    brokerage=brokerage,
                    policy=pol,
                    renewal_number=f'RN-{brokerage.pk}-{i+1}',
                    status=random.choice(['pending', 'renewed']),
                    previous_end_date=date.today(),
                    new_start_date=date.today() + timedelta(days=1),
                    new_end_date=date.today() + timedelta(days=366),
                    premium_value=random.uniform(500, 5000),
                )

                Endorsement.objects.create(
                    brokerage=brokerage,
                    policy=pol,
                    endorsement_number=f'EN-{brokerage.pk}-{i+1}',
                    endorsement_type=random.choice(['inclusion', 'alteration']),
                    description=f'Endosso de {pol}',
                    effective_date=date.today(),
                )

            pipeline = Pipeline.objects.create(brokerage=brokerage, name='Pipeline Principal')
            stage_names = ['Lead', 'Qualificado', 'Proposta', 'Negociacao', 'Fechado']
            stages = []

            for order, name in enumerate(stage_names):
                color = random.choice(['#3B82F6', '#8B5CF6', '#F59E0B', '#10B981', '#EF4444'])
                stage = PipelineStage.objects.create(brokerage=brokerage, pipeline=pipeline, name=name, color=color, order=order)
                stages.append(stage)

            for i in range(5):
                Deal.objects.create(
                    brokerage=brokerage,
                    pipeline=pipeline,
                    stage=random.choice(stages),
                    client=random.choice(clients),
                    title=f'NEG-{brokerage.pk}-{i+1} - {random.choice(clients).name}',
                    value=random.uniform(1000, 100000),
                    probability=random.randint(10, 100),
                )

            for i in range(2):
                agent = Agent.objects.create(
                    brokerage=brokerage,
                    name=f'Agente {i+1} da {brokerage}',
                    document=str(random.randint(10000000000, 99999999999)),
                    email=f'agente{i+1}@email.com',
                    commission_rate=random.uniform(5, 20),
                )

                for j in range(3):
                    Producer.objects.create(
                        brokerage=brokerage,
                        agent=agent if j == 0 else None,
                        name=f'Produtor {j+1} do Agente {i+1}',
                        document=str(random.randint(10000000000, 99999999999)),
                        commission_rate=random.uniform(3, 15),
                    )

            policy_with_comm = Policy.objects.filter(brokerage=brokerage).first()
            if policy_with_comm:
                from commissions.models import Commission
                for ct in ['received', 'passed']:
                    for k in range(2):
                        Commission.objects.create(
                            brokerage=brokerage,
                            policy=policy_with_comm,
                            commission_type=ct,
                            description=f'Comissao {ct} #{k+1}',
                            amount=random.uniform(100, 3000),
                            commission_date=date.today() - timedelta(days=random.randint(1, 90)),
                            status=random.choice(['pending', 'paid']),
                        )

            ct = ContentType.objects.get_for_model(Client)
            for c in clients[:3]:
                attach = Attachment(brokerage=brokerage, content_type=ct, object_id=c.pk, uploaded_by=owner)
                attach.original_filename = f'documento_{c.pk}.txt'
                attach.file.save(f'attachments/{brokerage.pk}/client/{c.pk}/doc.txt', ContentFile(b'Conteudo ficticio do anexo.'), save=True)

        self.stdout.write(self.style.SUCCESS(f'Dados ficticios gerados: {Brokerage.objects.count()} corretoras, {Client.objects.count()} clientes, {Policy.objects.count()} apolices, {Proposal.objects.count()} propostas.'))
