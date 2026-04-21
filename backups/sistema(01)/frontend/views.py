from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import UsuarioCustom
from backend.models import Anime
from dashboard_cliente.views import dashboard
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count


"""def home(request):
    user = None

    user_id = request.session.get('user_id')
    if user_id:
        user = UsuarioCustom.objects.filter(id=user_id).first()

    # lista de animes
    animes = Anime.objects.prefetch_related('generos', 'volumes__capitulos')

    # 🔥 pega slug da URL
    anime_slug = request.GET.get('anime')
    anime_selecionado = None

    if anime_slug:
        anime_selecionado = Anime.objects.filter(slug=anime_slug)\
            .prefetch_related('generos', 'volumes__capitulos')\
            .first()

    return render(request, 'anime/layout.html', {
        'user': user,
        'animes': animes,
        'anime_selecionado': anime_selecionado
    })"""

"""def home(request):
    user = UsuarioCustom.objects.filter(
        id=request.session.get('user_id')
    ).first()

    # lista de animes (já otimizada)
    animes = Anime.objects.prefetch_related(
        'generos',
        'volumes__capitulos'
    )

    # slug vindo da URL (?anime=naruto)
    anime_slug = request.GET.get('anime')

    anime_selecionado = None

    if anime_slug:
        anime_selecionado = animes.filter(slug=anime_slug).first()


    recentes = Anime.objects.order_by('-atualizado_em')[:10]

    return render(request, 'anime/layout.html', {
        'user': user,
        'animes': animes,
        'anime_selecionado': anime_selecionado,
        'recentes': recentes
    })"""

def home(request):
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

    # 🔥 RECENTES (já ordenado)
    recentes = animes[:20]

    return render(request, 'anime/layout.html', {
        'user': user,
        'animes': animes,
        'anime_selecionado': anime_selecionado,
        'recentes': recentes,
        'animes_normal': animes_normal,
    })


def registrar(request):
    return render(request, 'login/registrar.html')


"""def obra(request, slug):
    user = None

    user_id = request.session.get('user_id')

    if user_id:
        user = UsuarioCustom.objects.filter(id=user_id).first()

    anime = get_object_or_404(Anime, slug=slug)

    return render(request, 'anime/layout_anime.html', {
        'user': user,
        'anime': anime
    })"""

"""def obra(request, slug):
    user = None

    user_id = request.session.get('user_id')

    if user_id:
        user = UsuarioCustom.objects.filter(id=user_id).first()

    anime = get_object_or_404(Anime, slug=slug)

    

    return render(request, 'anime/layout_anime.html', {
        'user': user,
        'anime': anime
    })"""

"""def obra(request, slug):
    user = UsuarioCustom.objects.filter(
        id=request.session.get('user_id')
    ).first()

    anime = get_object_or_404(
        Anime.objects.annotate(
            total_capitulos=Count('volumes__capitulos')
        ).prefetch_related(
            'generos'  # leve
        ),
        slug=slug
    )

    return render(request, 'anime/layout_anime.html', {
        'user': user,
        'anime': anime
    })"""

def obra(request, slug):
    user = UsuarioCustom.objects.filter(
        id=request.session.get('user_id')
    ).first()

    anime = get_object_or_404(
        Anime.objects.prefetch_related('generos'),
        slug=slug
    )

    # 🔥 PEGAR GÊNEROS DO ANIME ATUAL
    generos = anime.generos.all()

    # 🔥 SUGERIDOS
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