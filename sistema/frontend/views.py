from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import UsuarioCustom
from dashboard_cliente.views import dashboard
from django.http import JsonResponse


def home(request):
    user = None

    user_id = request.session.get('user_id')

    if user_id:
        user = UsuarioCustom.objects.filter(id=user_id).first()

    return render(request, 'anime/layout.html', {
        'user': user
    })


def registrar(request):
    return render(request, 'login/registrar.html')


def obra(request):
    user = None

    user_id = request.session.get('user_id')

    if user_id:
        user = UsuarioCustom.objects.filter(id=user_id).first()

    return render(request, 'anime/layout_anime.html', {
        'user': user
    })