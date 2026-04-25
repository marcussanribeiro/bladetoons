from django.contrib import admin
from django.utils.html import format_html

from backend.model.model_anime import (
    Anime, Genero, Volume, Capitulo, Pagina
)

from django.core.exceptions import ValidationError

# =========================================================
# 🖼 PÁGINAS (INLINE DO CAPÍTULO)
# =========================================================
class PaginaInline(admin.TabularInline):
    model = Pagina
    extra = 1
    fields = ('numero', 'imagem')


# =========================================================
# 📖 CAPÍTULOS (INLINE DO VOLUME)
# =========================================================
class CapituloInline(admin.TabularInline):
    model = Capitulo
    extra = 0
    fields = ('numero', 'titulo', 'visualizacoes')
    readonly_fields = ('visualizacoes',)

    def clean(self):
        if Capitulo.objects.filter(volume=self.volume, numero=self.numero).exists():
            raise ValidationError('Já existe um capítulo com esse número neste volume.')


# =========================================================
# 📚 VOLUMES (INLINE DO ANIME)
# =========================================================
class VolumeInline(admin.TabularInline):
    model = Volume
    extra = 0
    fields = ('numero',)


# =========================================================
# 🎬 ANIME (PAINEL PRINCIPAL COMPLETO)
# =========================================================
@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):

    list_display = ('titulo', 'criado_em', 'atualizado_em', 'preview_capa')
    search_fields = ('titulo',)
    ordering = ('-atualizado_em',)

    # 🔥 Hierarquia principal
    inlines = [VolumeInline]

    def preview_capa(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" width="50" style="border-radius:6px;" />',
                obj.imagem.url
            )
        return "Sem imagem"

    preview_capa.short_description = "Capa"


# =========================================================
# 📚 VOLUME (COM CAPÍTULOS)
# =========================================================
@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):

    list_display = ('anime', 'numero')
    search_fields = ('anime__titulo',)
    list_filter = ('anime',)

    inlines = [CapituloInline]


# =========================================================
# 📖 CAPÍTULO (COM PÁGINAS)
# =========================================================
@admin.register(Capitulo)
class CapituloAdmin(admin.ModelAdmin):

    list_display = (
        'titulo',
        'numero',
        'volume',
        'visualizacoes',
        'total_paginas'
    )

    search_fields = (
        'titulo',
        'volume__anime__titulo'
    )

    list_filter = (
        'volume__anime',
        'volume'
    )

    inlines = [PaginaInline]

    def total_paginas(self, obj):
        return obj.paginas.count()

    total_paginas.short_description = "Páginas"


# =========================================================
# 🖼 PÁGINAS
# =========================================================
@admin.register(Pagina)
class PaginaAdmin(admin.ModelAdmin):

    list_display = ('capitulo', 'numero', 'preview')
    list_filter = ('capitulo__volume__anime',)
    ordering = ('capitulo', 'numero')

    def preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" width="60" style="border-radius:4px;" />',
                obj.imagem.url
            )
        return "-"

    preview.short_description = "Preview"


# =========================================================
# 🏷 GÊNEROS
# =========================================================
@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nome',)