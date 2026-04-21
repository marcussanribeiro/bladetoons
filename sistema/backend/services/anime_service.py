from backend.model.model_anime import CapituloView, Capitulo
from django.db.models import F

def registrar_view(capitulo, user=None):
    CapituloView.objects.create(
        capitulo=capitulo,
        user=user
    )

    # mantém contador antigo também
    Capitulo.objects.filter(id=capitulo.id).update(
        visualizacoes=F('visualizacoes') + 1
    )