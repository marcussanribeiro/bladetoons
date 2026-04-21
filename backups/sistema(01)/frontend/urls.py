from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, registrar, obra

app_name = 'frontend'

urlpatterns = [
    path('', home, name='home'),
    #path('login/', login, name='login'),
    path('registrar/', registrar, name='registrar'),
    path('obra/<slug:slug>/', obra , name='obra'),
    
]