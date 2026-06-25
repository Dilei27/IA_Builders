from django.contrib import admin


class TenantAdminMixin:
    tenant_field = 'brokerage'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        brokerage = getattr(request.user, 'brokerage', None)
        if brokerage is None:
            return queryset.none()

        return queryset.filter(**{self.tenant_field: brokerage})

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not getattr(obj, self.tenant_field, None):
            setattr(obj, self.tenant_field, request.user.brokerage)

        super().save_model(request, obj, form, change)


class TenantFilter(admin.SimpleListFilter):
    title = 'corretora'
    parameter_name = 'brokerage'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            from core.models import Brokerage
            return Brokerage.objects.values_list('pk', 'legal_name')

        brokerage = getattr(request.user, 'brokerage', None)
        if brokerage:
            return ((brokerage.pk, str(brokerage)),)

        return ()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(brokerage=self.value())

        return queryset
