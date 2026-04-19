from django.http import JsonResponse
from backend.model.model_accounts import UsuarioCustom 
from django.utils.http import url_has_allowed_host_and_scheme

"""def login_api(request):
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

    return JsonResponse({'success': False})"""


def login_api(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or request.GET.get('next')

        if not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Preencha todos os campos'
            })

        try:
            user = UsuarioCustom.objects.get(email=email.strip().lower())

            if user.check_senha(password):
                # 🔐 salva sessão
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email

                # 🔁 valida o next (segurança)
                if next_url and url_has_allowed_host_and_scheme(
                    next_url, allowed_hosts={request.get_host()}
                ):
                    redirect_url = next_url
                else:
                    redirect_url = '/'

                return JsonResponse({
                    'success': True,
                    'redirect': redirect_url
                })

            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Senha incorreta'
                })

        except UsuarioCustom.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Email ou senha inválidos'
            })

    return JsonResponse({
        'success': False,
        'error': 'Método inválido'
    })