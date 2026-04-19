from rest_framework import viewsets
from backend.model.model_anime import Anime
from backend.serializer.serializer_anime import AnimeSerializer
from django.http import FileResponse, Http404
from django.conf import settings
import os
from django.shortcuts import render, get_object_or_404
from frontend.models import UsuarioCustom
from django.http import JsonResponse


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


"""def obra(request, slug):
    return render(request, 'layout_anime.html')"""

"""def obra(request, slug):
    user = None

    user_id = request.session.get('user_id')

    if user_id:
        user = UsuarioCustom.objects.filter(id=user_id).first()

    # 🔥 busca pelo slug
    anime = get_object_or_404(Anime, slug=slug)

    return render(request, 'anime/layout_anime.html', {
        'user': user,
        'anime': anime
    })"""

def obra_api(request, slug):
    anime = get_object_or_404(Anime, slug=slug)

    data = {
        'id': anime.id,
        'titulo': anime.titulo,
        'slug': anime.slug,
        'descricao': anime.descricao,
        'capa': anime.capa.url if anime.capa else None,
    }

    return JsonResponse(data)