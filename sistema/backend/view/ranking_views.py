from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from backend.model.model_anime import Anime
from django.db.models import Sum




def ranking_animes_api(request):

    periodo = request.GET.get("periodo", "mes")

    now = timezone.now()

    if periodo == "hoje":
        inicio = now - timedelta(days=1)
    elif periodo == "semana":
        inicio = now - timedelta(days=7)
    else:
        inicio = now - timedelta(days=30)

    animes = (
        Anime.objects.annotate(
            total_views=Sum(
                'volumes__capitulos__visualizacoes'
            )
        )
        .order_by('-total_views')[:10]
    )

    data = [
        {
            "id": a.id,
            "titulo": a.titulo,
            "slug": a.slug,
            "imagem": a.imagem.url if a.imagem else None,
            "total_views": a.total_views or 0
        }
        for a in animes
    ]

    return JsonResponse({"results": data})