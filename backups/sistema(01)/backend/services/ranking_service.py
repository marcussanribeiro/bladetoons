from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from backend.model.model_anime import Anime

def ranking_anime(request):

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
    total_views=Count(
        'volumes__capitulos__views',
        filter=Q(
            volumes__capitulos__views__created_at__gte=inicio
        )
    )
)
.order_by('-total_views')[:10])