from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import dashboard, logout

app_name = 'dashboard_cliente'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('logout/', logout, name='logout')
]