from django.db import models

from .managers import TenantManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseTenantModel(BaseModel):
    brokerage = models.ForeignKey(
        'core.Brokerage',
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_set',
    )

    objects = TenantManager()

    class Meta:
        abstract = True
