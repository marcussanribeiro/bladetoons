from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, registrar, obra


urlpatterns = [
    path('', home, name='home'),
    #path('login/', login, name='login'),
    path('registrar/', registrar, name='registrar'),
    path('obra/', obra , name='obra'),
]