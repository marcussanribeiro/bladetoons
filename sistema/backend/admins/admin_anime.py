from django.contrib import admin
from backend.model.model_anime import Anime, Genero
from django.utils.html import format_html

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ver_pdf')
    search_fields = ('titulo',)

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


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nome',)