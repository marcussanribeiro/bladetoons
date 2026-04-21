from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from backend.view.login_view import login_api
from backend.view.ranking_views import ranking_animes_api

app_name = 'api'

urlpatterns = [
    path('login/', include('backend.url.url_login')),
    path('anime/', include(('backend.url.url_anime', 'anime'), namespace='anime')),
    path( 'dashboard/', include(('backend.url.url_dashboard_cliente', 'dashboard_cliente'), namespace='dashboard_cliente')),
    path("ranking-animes/", ranking_animes_api, name="ranking_animes_api"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)