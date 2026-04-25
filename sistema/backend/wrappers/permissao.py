from django.http import HttpResponseForbidden
from backend.model.model_accounts import UsuarioCustom

def permissao_necessaria(nome_permissao):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_id = request.session.get('user_id')

            if not user_id:
                return HttpResponseForbidden('Não autenticado')

            user = UsuarioCustom.objects.get(id=user_id)

            if not user.tem_permissao(nome_permissao):
                return HttpResponseForbidden('Sem permissão')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator