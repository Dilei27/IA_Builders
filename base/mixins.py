from django.core.exceptions import PermissionDenied


class TenantQuerysetMixin:
    tenant_field = 'brokerage'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return queryset

        brokerage = getattr(self.request, 'brokerage', None)
        if brokerage is None:
            return queryset.none()

        return queryset.filter(**{self.tenant_field: brokerage})


class TenantObjectMixin:
    tenant_field = 'brokerage'

    def validate_object_tenant(self, obj):
        user = self.request.user

        if user.is_superuser:
            return obj

        if getattr(obj, self.tenant_field) != getattr(self.request, 'brokerage', None):
            raise PermissionDenied('Object does not belong to the current tenant.')

        return obj
