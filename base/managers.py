from django.db import models


class TenantQuerySet(models.QuerySet):
    def for_brokerage(self, brokerage):
        if brokerage is None:
            return self.none()

        return self.filter(brokerage=brokerage)

    def for_request(self, request):
        return self.for_brokerage(getattr(request, 'brokerage', None))


class TenantManager(models.Manager.from_queryset(TenantQuerySet)):
    pass
