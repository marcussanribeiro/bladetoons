from rest_framework import viewsets
from backend.model.model_anime import Anime
from backend.serializer.serializer_anime import AnimeSerializer
from django.http import FileResponse, Http404
from django.conf import settings
import os
from django.shortcuts import render, get_object_or_404
from frontend.models import UsuarioCustom
from django.http import JsonResponse
from backend.model.model_anime import CapituloLido, Capitulo
from django.db.models import F


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

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

def obra_api(request, slug):

    anime = get_object_or_404(
        Anime.objects.prefetch_related(
            Prefetch(
                'volumes__capitulos__paginas'
            )
        ),
        slug=slug
    )

    usuario_id = request.session.get('user_id')

    lidos = set()

    if usuario_id:
        lidos = set(
            CapituloLido.objects.filter(
                user_id=usuario_id,
                lido=True,
                capitulo__volume__anime=anime
            ).values_list('capitulo_id', flat=True)
        )

    volumes_data = []

    for volume in anime.volumes.all().order_by('numero'):

        capitulos_data = []

        for cap in volume.capitulos.all().order_by('numero'):

            cap_data = {
                'id': cap.id,
                'numero': cap.numero,
                'titulo': cap.titulo,

                # 🔥 adiciona quantidade de páginas (leve pro frontend)
                'total_paginas': cap.paginas.count(),
            }

            # 🔥 lido só se logado
            if usuario_id:
                cap_data['lido'] = cap.id in lidos

            capitulos_data.append(cap_data)

        volumes_data.append({
            'id': volume.id,
            'numero': volume.numero,
            'capitulos': capitulos_data
        })

    return JsonResponse({
        'id': anime.id,
        'titulo': anime.titulo,
        'slug': anime.slug,
        'descricao': anime.descricao,
        'capa': anime.imagem.url if anime.imagem else None,
        'total_capitulos': sum(len(v['capitulos']) for v in volumes_data),
        'volumes': volumes_data,
    })


def paginas_capitulo(request, capitulo_id):

    cap = get_object_or_404(
        Capitulo.objects.prefetch_related('paginas'),
        id=capitulo_id
    )

    paginas = [
        pagina.imagem.url
        for pagina in cap.paginas.all()
    ]

    return JsonResponse({
        'id': cap.id,
        'titulo': cap.titulo,
        'paginas': paginas
    })

