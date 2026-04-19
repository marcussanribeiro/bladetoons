from django.shortcuts import render, redirect
from backend.model.model_accounts import UsuarioCustom


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
