from django.http import JsonResponse
from backend.model.model_accounts import UsuarioCustom 

def login_api(request):
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