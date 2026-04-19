from django.contrib import admin
from django.utils.html import format_html

from backend.model.model_anime import Anime, Genero, Volume, Capitulo


# 🔥 INLINE DE CAPÍTULOS (dentro do Volume)
class CapituloInline(admin.TabularInline):
    model = Capitulo
    extra = 0
    fields = ('numero', 'titulo', 'pdf', 'visualizacoes')
    readonly_fields = ('visualizacoes',)


# 🔥 ADMIN DE VOLUME (com capítulos dentro)
@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_display = ('anime', 'numero')
    search_fields = ('anime__titulo',)
    inlines = [CapituloInline]


# 🔥 INLINE DE VOLUMES (dentro do Anime)
class VolumeInline(admin.TabularInline):
    model = Volume
    extra = 0
    fields = ('numero',)


# 🔥 ADMIN DE ANIME
@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'criado_em' ,'atualizado_em', 'ver_pdf')
    search_fields = ('titulo',)
    ordering = ('-atualizado_em',)
    inlines = [VolumeInline]

    def ver_pdf(self, obj):
        volume = obj.volumes.first()
        if not volume:
            return "Sem volume"

        capitulo = volume.capitulos.first()
        if not capitulo or not capitulo.pdf:
            return "Sem PDF"

        return format_html(
            '<a href="{}" target="_blank">Ver PDF</a>',
            capitulo.pdf.url
        )

    ver_pdf.short_description = "PDF"


# 🔥 ADMIN DE CAPÍTULO (opcional, mas útil)
@admin.register(Capitulo)
class CapituloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'numero', 'volume', 'visualizacoes')
    search_fields = ('titulo',)
    list_filter = ('volume',)


# 🔥 ADMIN DE GÊNERO
@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nome',)