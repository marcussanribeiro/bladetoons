from django.shortcuts import render, redirect
from backend.model.model_accounts import UsuarioCustom
from backend.model.model_anime import CapituloLido, Capitulo
from django.http import JsonResponse
from django.db.models import F
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from functools import wraps



#def login_required_custom(view_func)
"""def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper"""

def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('/')

        if not UsuarioCustom.objects.filter(id=user_id).exists():
            request.session.flush()
            return redirect('/')

        return view_func(request, *args, **kwargs)

    return wrapper