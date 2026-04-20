from django.contrib import admin
from backend.model.model_accounts import UsuarioCustom
from backend.model.model_anime import CapituloLido


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


@admin.register(CapituloLido)
class CapituloLidoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'capitulo',
        'lido',
        'data_leitura',
    )

    list_filter = (
        'lido',
        'data_leitura',
        'user',
    )

    search_fields = (
        'user__username',
        'capitulo__titulo',
    )

    ordering = (
        '-data_leitura',
    )

    autocomplete_fields = (
        'user',
        'capitulo',
    )