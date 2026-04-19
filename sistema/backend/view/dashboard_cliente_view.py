from django.shortcuts import render, redirect
from backend.model.model_accounts import UsuarioCustom
from backend.model.model_accounts import CapituloLido
from backend.model.model_anime import Capitulo
from django.http import JsonResponse


def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_custom
def dashboard(request):
    user_id = request.session.get('user_id')

    if user_id:
        user = UsuarioCustom.objects.get(id=user_id)
        context = {'user': user}
        return render(request, 'dashboard_cliente/dashboard/dashboard.html', context)
    

def logout(request):
    request.session.flush()
    return redirect('frontend:home')


"""@login_required_custom
def marcar_lido(request, cap_id):

    usuario_id = request.session.get('user_id')

    if not usuario_id:
        return JsonResponse({'erro': 'sem sessão'}, status=403)

    try:
        usuario = UsuarioCustom.objects.get(id=usuario_id)
        cap = Capitulo.objects.get(id=cap_id)

    except UsuarioCustom.DoesNotExist:
        return JsonResponse({'erro': 'usuário inválido'}, status=400)

    except Capitulo.DoesNotExist:
        return JsonResponse({'erro': 'capítulo inválido'}, status=400)

    # 🔥 busca registro real
    obj = CapituloLido.objects.filter(
        user=usuario,
        capitulo=cap
    ).first()

    # 🔥 se não existe → cria como TRUE
    if obj is None:
        obj = CapituloLido.objects.create(
            user=usuario,
            capitulo=cap,
            lido=True
        )
    else:
        # 🔥 alterna estado real
        obj.lido = not obj.lido
        obj.save()

    return JsonResponse({
        'lido': obj.lido,
        'cap_id': cap_id
    })"""

@login_required_custom
def marcar_lido(request, cap_id):

    usuario_id = request.session.get('user_id')

    if not usuario_id:
        return JsonResponse({'erro': 'sem sessão'}, status=403)

    try:
        usuario = UsuarioCustom.objects.get(id=usuario_id)
    except UsuarioCustom.DoesNotExist:
        return JsonResponse({'erro': 'usuário inválido'}, status=400)

    try:
        cap = Capitulo.objects.get(id=cap_id)
    except Capitulo.DoesNotExist:
        return JsonResponse({'erro': 'capítulo inválido'}, status=400)

    obj, created = CapituloLido.objects.get_or_create(
        user=usuario,
        capitulo=cap,
        defaults={'lido': True}
    )

    if not created:
        obj.lido = not obj.lido
        obj.save()

    return JsonResponse({
        'lido': obj.lido
    })

