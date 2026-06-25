from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.views import View

from base.mixins import TenantQuerysetMixin
from clients.models import Client
from crm.models import Deal, PipelineStage
from insurers.models import Insurer
from policies.models import Policy, Proposal


class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        brokerage = request.brokerage
        qs_kwargs = {'brokerage': brokerage} if brokerage else {}

        client_count = Client.objects.filter(**qs_kwargs).count()
        insurer_count = Insurer.objects.filter(**qs_kwargs).count()
        proposal_count = Proposal.objects.filter(**qs_kwargs).count()
        policy_count = Policy.objects.filter(**qs_kwargs).count()

        proposals_by_status = (
            Proposal.objects.filter(**qs_kwargs)
            .values('status')
            .annotate(total=Count('pk'))
            .order_by('status')
        )

        policies_by_status = (
            Policy.objects.filter(**qs_kwargs)
            .values('status')
            .annotate(total=Count('pk'))
            .order_by('status')
        )

        stages = PipelineStage.objects.filter(**qs_kwargs, is_active=True).order_by('order')

        deals_by_stage = []

        for stage in stages:
            count = Deal.objects.filter(**qs_kwargs, stage=stage, is_active=True).count()
            deals_by_stage.append({'name': stage.name, 'count': count, 'color': stage.color})

        total_deals = sum(d['count'] for d in deals_by_stage)
        max_deals = max((d['count'] for d in deals_by_stage), default=1)

        for d in deals_by_stage:
            d['width_pct'] = int((d['count'] / max_deals) * 100) if max_deals else 0

        context = {
            'client_count': client_count,
            'insurer_count': insurer_count,
            'proposal_count': proposal_count,
            'policy_count': policy_count,
            'proposals_by_status': proposals_by_status,
            'policies_by_status': policies_by_status,
            'deals_by_stage': deals_by_stage,
            'total_deals': total_deals,
        }
        return render(request, self.template_name, context)
