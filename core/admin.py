from django.contrib import admin

from .models import Brokerage, User


class TenantBrokerageListFilter(admin.SimpleListFilter):
    title = 'corretora'
    parameter_name = 'brokerage'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            from .models import Brokerage
            return Brokerage.objects.values_list('pk', 'legal_name')

        brokerage = getattr(request.user, 'brokerage', None)
        if brokerage:
            return ((brokerage.pk, brokerage.legal_name),)

        return ()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(brokerage=self.value())

        return queryset


@admin.register(Brokerage)
class BrokerageAdmin(admin.ModelAdmin):
    list_display = ('legal_name', 'trade_name', 'cnpj', 'plan', 'is_active')
    list_filter = ('plan', 'is_active')
    search_fields = ('legal_name', 'trade_name', 'cnpj', 'email')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Dados pessoais', {'fields': ('full_name', 'brokerage', 'role')}),
        ('Permissoes', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
    )
    list_display = ('email', 'full_name', 'brokerage', 'role', 'is_staff', 'is_active')
    list_filter = ('brokerage', 'role', 'is_staff', 'is_active', 'is_superuser', 'groups')
    search_fields = ('email', 'full_name', 'brokerage__legal_name', 'brokerage__cnpj')
    ordering = ('email',)


admin.site.site_title = 'SCSI Admin'
admin.site.site_header = 'SCSI - Sistema de Gestao para Corretora de Seguros'
admin.site.index_title = 'Administracao do sistema'
