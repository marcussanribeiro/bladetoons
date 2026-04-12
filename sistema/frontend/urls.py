from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, login, registrar


urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('registrar/', registrar, name='registrar'),
]