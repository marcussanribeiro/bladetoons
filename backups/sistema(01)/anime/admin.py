from django.contrib import admin
from .models import Anime

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ver_pdf')
    search_fields = ('titulo',)
    #filter_horizontal = ('generos',)

    def ver_pdf(self, obj):
        if obj.pdf:
            return f"/anime/pdf/{obj.pdf.name.split('/')[-1]}"
        return "Sem PDF"

    ver_pdf.short_description = "PDF"


"""@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nome',)"""