from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.view.dashboard_cliente_view import dashboard, logout


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('logout/', logout, name='logout')
]