from django.shortcuts import render, redirect
from backend.model.model_accounts import UsuarioCustom
from backend.model.model_anime import CapituloLido
from backend.model.model_anime import Capitulo
from django.http import JsonResponse
from django.db.models import F
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404


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



@require_POST
def marcar_lido(request, capitulo_id):

    user_id = request.session.get('user_id')

    if not user_id:
        return JsonResponse({'error': 'não autenticado'}, status=403)

    usuario = get_object_or_404(UsuarioCustom, id=user_id)
    cap = get_object_or_404(Capitulo, id=capitulo_id)

    obj, created = CapituloLido.objects.get_or_create(
        user=usuario,
        capitulo=cap,
        defaults={'lido': True}
    )

    # 🔥 se já existe e já está lido → não faz nada
    if not created and obj.lido:
        return JsonResponse({
            'status': 'ja_marcado'
        })

    # 🔥 se existe mas estava falso → ativa
    if not obj.lido:
        obj.lido = True
        obj.save()

    # 🔥 incrementa apenas UMA vez por usuário
    if created:
        Capitulo.objects.filter(id=cap.id).update(
            visualizacoes=F('visualizacoes') + 1
        )

    return JsonResponse({
        'status': 'ok'
    })
