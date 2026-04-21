from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.view.anime_view import AnimeViewSet, ver_pdf, obra_api, paginas_capitulo, search_animes

app_name = 'anime'

router = DefaultRouter()
router.register(r'animes', AnimeViewSet, basename='animes')

urlpatterns = [
    path('', include(router.urls)),  # 👈 API
    path('pdf/<str:nome_arquivo>/', ver_pdf, name='ver_pdf'),
    path("search/", search_animes, name="search_animes"),
    path('<slug:slug>/', obra_api, name='obra_api'),
    path('capitulo/<int:capitulo_id>/', paginas_capitulo, name='revista'),
    
]