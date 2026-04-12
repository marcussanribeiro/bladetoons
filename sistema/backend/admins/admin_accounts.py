from django.contrib import admin
from backend.model.model_accounts import UsuarioCustom


@admin.register(UsuarioCustom)
class UsuarioCustomAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'entidade', 'vip', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('vip', 'entidade')
    ordering = ('-created_at',)

    fieldsets = (
        ('Dados do Usuário', {
            'fields': ('username', 'email', 'senha')
        }),
        ('Configurações', {
            'fields': ('entidade', 'vip')
        }),
    )