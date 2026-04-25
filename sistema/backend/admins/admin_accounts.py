from django.contrib import admin
from backend.model.model_accounts import UsuarioCustom, Grupo, Permissao
from backend.model.model_anime import CapituloLido


@admin.register(Permissao)
class PermissaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    filter_horizontal = ('permissoes',)  # 🔥 MUITO IMPORTANTE

@admin.register(UsuarioCustom)
class UsuarioCustomAdmin(admin.ModelAdmin):

    list_display = ('username', 'email', 'vip', 'created_at')
    list_filter = ('vip',)
    search_fields = ('username', 'email')

    filter_horizontal = ('grupos',)  # 🔥 ESSENCIAL

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