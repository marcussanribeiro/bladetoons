from django.contrib import admin
from django.utils.html import format_html

from backend.model.model_anime import Anime, Genero, Volume, Capitulo, Pagina


# =========================
# 🔥 INLINE DE PÁGINAS (dentro do Capítulo)
# =========================
class PaginaInline(admin.TabularInline):
    model = Pagina
    extra = 1
    fields = ('numero', 'imagem')


# =========================
# 🔥 INLINE DE CAPÍTULOS (dentro do Volume)
# =========================
class CapituloInline(admin.TabularInline):
    model = Capitulo
    extra = 0
    fields = ('numero', 'titulo', 'visualizacoes')
    readonly_fields = ('visualizacoes',)


# =========================
# 🔥 ADMIN DE VOLUME
# =========================
@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_display = ('anime', 'numero')
    search_fields = ('anime__titulo',)
    inlines = [CapituloInline]


# =========================
# 🔥 INLINE DE VOLUMES (dentro do Anime)
# =========================
class VolumeInline(admin.TabularInline):
    model = Volume
    extra = 0
    fields = ('numero',)


# =========================
# 🔥 ADMIN DE ANIME
# =========================
@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'criado_em', 'atualizado_em', 'preview_capa')
    search_fields = ('titulo',)
    ordering = ('-atualizado_em',)
    inlines = [VolumeInline]

    def preview_capa(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="50" />', obj.imagem.url)
        return "Sem imagem"

    preview_capa.short_description = "Capa"


# =========================
# 🔥 ADMIN DE CAPÍTULO
# =========================
@admin.register(Capitulo)
class CapituloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'numero', 'volume', 'visualizacoes', 'total_paginas')
    search_fields = ('titulo',)
    list_filter = ('volume',)
    inlines = [PaginaInline]

    def total_paginas(self, obj):
        return obj.paginas.count()

    total_paginas.short_description = "Páginas"


# =========================
# 🔥 ADMIN DE PÁGINA
# =========================
@admin.register(Pagina)
class PaginaAdmin(admin.ModelAdmin):
    list_display = ('capitulo', 'numero')
    list_filter = ('capitulo',)
    ordering = ('capitulo', 'numero')

    def preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="60" />', obj.imagem.url)
        return "-"

    preview.short_description = "Preview"


# =========================
# 🔥 ADMIN DE GÊNERO
# =========================
@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nome',)