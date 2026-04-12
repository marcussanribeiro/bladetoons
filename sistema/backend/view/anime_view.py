from rest_framework import viewsets
from backend.model.model_anime import Anime
from backend.serializer.serializer_anime import AnimeSerializer
from django.http import FileResponse, Http404
from django.conf import settings
import os
from django.shortcuts import render

class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer


def ver_pdf(request, nome_arquivo):
    caminho = os.path.join(settings.MEDIA_ROOT, 'pdfs', nome_arquivo)

    if not os.path.exists(caminho):
        raise Http404("PDF não encontrado")

    response = FileResponse(open(caminho, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nome_arquivo}"'

    return response


def obra(request):
    return render(request, 'layout_anime.html')