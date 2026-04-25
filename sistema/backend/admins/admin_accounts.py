from django.contrib import admin
from backend.model.model_accounts import UsuarioCustom
from backend.model.model_anime import CapituloLido


@admin.register(UsuarioCustom)
class UsuarioCustomAdmin(admin.ModelAdmin):

    list_display = ('username', 'email', 'vip', 'created_at')
    list_filter = ('vip',)

    search_fields = ('username', 'email')  # 👈 ESSENCIAL

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('username', 'email', 'senha')
        }),
        ('Permissões', {
            'fields': ('vip', 'grupos')
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