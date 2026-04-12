from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import UsuarioCustom
from dashboard_cliente.views import dashboard

# Create your views here.

def home(request):
    return render(request, 'anime/layout.html')


"""def login(request):
    return render(request, 'login/login.html')"""

"""def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Preencha todos os campos')
            return render(request, 'login/login.html')

        try:
            user = UsuarioCustom.objects.get(email=email.strip().lower())

            # DEBUG (pode remover depois)
            print("EMAIL:", email)
            print("SENHA DIGITADA:", password)
            print("SENHA SALVA:", user.senha)

            # comparação direta (SEM HASH, já que seu banco está assim)
            if user.senha == password:
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                return redirect('home')
            else:
                messages.error(request, 'Senha incorreta')

        except UsuarioCustom.DoesNotExist:
            messages.error(request, 'Usuário não encontrado')

    return render(request, 'login/login.html')"""

"""def login(request):
#correto
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Preencha todos os campos')
            return render(request, 'login/login.html')

        try:
            user = UsuarioCustom.objects.get(email=email.strip().lower())

            # DEBUG
            print("EMAIL:", email)
            print("SENHA DIGITADA:", password)
            print("HASH SALVO:", user.senha)

            # ✅ comparação correta
            if user.check_senha(password):
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                return redirect('dashboard')
            else:
                messages.error(request, 'Senha incorreta')

        except UsuarioCustom.DoesNotExist:
            messages.error(request, 'Usuário não encontrado')

    return render(request, 'login/login.html')"""

from django.http import JsonResponse

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return JsonResponse({'success': False, 'error': 'Preencha todos os campos'})

        try:
            user = UsuarioCustom.objects.get(email=email.strip().lower())

            if user.check_senha(password):
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Senha incorreta'})

        except UsuarioCustom.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Senha incorreta'})

    return JsonResponse({'success': False})

def registrar(request):
    return render(request, 'login/registrar.html')