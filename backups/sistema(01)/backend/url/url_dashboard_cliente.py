from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.view.dashboard_cliente_view import dashboard, logout, marcar_lido

app_name = 'dashboard_cliente'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('logout/', logout, name='logout'),
    path('capitulo/lido/<int:capitulo_id>/', marcar_lido, name='marcar_lido'),
]