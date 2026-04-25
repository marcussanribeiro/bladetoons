from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import UsuarioCustom
from backend.models import Anime
from dashboard_cliente.views import dashboard
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
import random
from django.db.models import Sum

from backend.model.model_accounts import UsuarioCustom
from backend.model.model_anime import Anime
from django.utils import timezone


"""def home(request):
    user = UsuarioCustom.objects.filter(
        id=request.session.get('user_id')
    ).first()

    animes = Anime.objects.prefetch_related(
        'generos',
        'volumes__capitulos'
    ).order_by('-atualizado_em')
    animes_normal = Anime.objects.prefetch_related(
        'generos',
        'volumes__capitulos'
    ).order_by('-criado_em')

    anime_slug = request.GET.get('anime')

    anime_selecionado = None

    if anime_slug:
        anime_selecionado = animes.filter(slug=anime_slug).first()

    #  RECENTES (já ordenado)
    recentes = animes[:20]

    ids = list(Anime.objects.exclude(imagem='').values_list('id', flat=True))

    if ids:
        random_ids = random.sample(ids, min(len(ids), 5))
        slides = Anime.objects.filter(id__in=random_ids)
    else:
        slides = []

    return render(request, 'anime/layout.html', {
        'user': user,
        'animes': animes,
        'anime_selecionado': anime_selecionado,
        'recentes': recentes,
        'animes_normal': animes_normal,
        'slides': slides
    })"""

def home(request):
    # 👤 USUÁRIO
    user = UsuarioCustom.objects.filter(
        id=request.session.get('user_id')
    ).first()

    # 📚 BASE DE ANIMES
    animes = Anime.objects.prefetch_related(
        'generos',
        'volumes__capitulos'
    ).order_by('-atualizado_em')

    animes_normal = Anime.objects.prefetch_related(
        'generos',
        'volumes__capitulos'
    ).order_by('-criado_em')

    # 🎯 ANIME SELECIONADO
    anime_slug = request.GET.get('anime')
    anime_selecionado = None

    if anime_slug:
        anime_selecionado = animes.filter(slug=anime_slug).first()

    # 🔥 RECENTES
    recentes = animes[:20]

    # =========================
    # 🎬 SLIDES INTELIGENTES (24h)
    # =========================

    hoje = timezone.now().date()

    # session para evitar repetição por 24h
    slides_cache = request.session.get('slides_cache', {})
    cache_data = slides_cache.get('data')
    cache_ids = slides_cache.get('ids', [])

    if cache_data == str(hoje) and cache_ids:
        slides = Anime.objects.filter(id__in=cache_ids)

    else:
        # 📊 POPULARES (5)
        populares = (
            Anime.objects.annotate(
                total_views=Sum('volumes__capitulos__visualizacoes')
            )
            .order_by('-total_views')
            .exclude(imagem='')
        )[:5]

        # 🧊 MENOS VISTOS (5)
        menos_vistos = (
            Anime.objects.annotate(
                total_views=Sum('volumes__capitulos__visualizacoes')
            )
            .order_by('total_views')
            .exclude(imagem='')
        )[:5]

        # 🔥 JUNTA E REMOVE DUPLICADOS
        ids = list({anime.id for anime in list(populares) + list(menos_vistos)})

        # ⚠️ garante no máximo 10
        ids = ids[:10]

        # embaralha (opcional, deixa mais dinâmico)
        random.shuffle(ids)

        slides = Anime.objects.filter(id__in=ids)

        # 💾 salva na sessão por 24h
        request.session['slides_cache'] = {
            'data': str(hoje),
            'ids': ids
        }

    # =========================

    return render(request, 'anime/layout.html', {
        'user': user,
        'animes': animes,
        'anime_selecionado': anime_selecionado,
        'recentes': recentes,
        'animes_normal': animes_normal,
        'slides': slides
    })


def registrar(request):
    return render(request, 'login/registrar.html')



def obra(request, slug):
    user = UsuarioCustom.objects.filter(
        id=request.session.get('user_id')
    ).first()

    anime = get_object_or_404(
        Anime.objects.prefetch_related('generos'),
        slug=slug
    )

#PEGAR GÊNEROS DO ANIME ATUAL
    generos = anime.generos.all()

# SUGERIDOS
    sugeridos = Anime.objects.filter(
        generos__in=generos
    ).exclude(
        id=anime.id
    ).distinct().annotate(
        match_count=Count('generos')
    ).order_by('-match_count')[:8]  # limite

    return render(request, 'anime/layout_anime.html', {
        'user': user,
        'anime': anime,
        'sugeridos': sugeridos
    })