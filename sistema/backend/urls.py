from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from backend.view.login_view import login_api

app_name = 'api'

urlpatterns = [
    path('login/', include('backend.url.url_login')),
    #path('login/', login_api, name='login'),
    path('dashboard/', include('backend.url.url_dashboard_cliente')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)