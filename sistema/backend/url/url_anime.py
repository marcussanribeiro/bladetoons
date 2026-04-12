from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.view.anime_view import AnimeViewSet, ver_pdf, obra

router = DefaultRouter()
router.register(r'animes', AnimeViewSet, basename='animes')

urlpatterns = [
    path('', include(router.urls)),  # 👈 API
    path('pdf/<str:nome_arquivo>/', ver_pdf, name='ver_pdf'),  # 👈 PDF
    path('obra/', obra , name='obra'),
]