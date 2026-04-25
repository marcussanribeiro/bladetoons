from django.shortcuts import render, redirect
from backend.model.model_accounts import UsuarioCustom
from backend.model.model_anime import CapituloLido, Capitulo
from django.http import JsonResponse
from django.db.models import F
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from backend.wrappers.login_required import login_required_custom
from django.http import HttpResponseForbidden



@login_required_custom
def dashboard_admin(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = UsuarioCustom.objects.get(id=user_id)

    # 🔒 VERIFICA PERMISSÃO
    if not user.tem_permissao('acessar_dashboard_admin'):
        return HttpResponseForbidden('Você não tem permissão para acessar o dashboard.')

    context = {'user': user}
    return render(request, 'dashboard_cliente/dashboard/dashboard.html', context)
    

def logout(request):
    request.session.flush()
    return redirect('frontend:home')



"""@require_POST
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

    #  se já existe e já está lido → não faz nada
    if not created and obj.lido:
        return JsonResponse({
            'status': 'ja_marcado'
        })

    # se existe mas estava falso → ativa
    if not obj.lido:
        obj.lido = True
        obj.save()

    #  incrementa apenas UMA vez por usuário
    if created:
        Capitulo.objects.filter(id=cap.id).update(
            visualizacoes=F('visualizacoes') + 1
        )

    return JsonResponse({
        'status': 'ok'
    })"""


