from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Capitulo, Anime
from django.utils import timezone


def atualizar(anime):
    print("🔥 [DEBUG] Entrou na função atualizar()")

    total = Capitulo.objects.filter(volume__anime=anime).count()

    print(f"🔥 [DEBUG] Total calculado: {total} para anime ID {anime.id}")

    Anime.objects.filter(id=anime.id).update(total_capitulos=total)

    print("🔥 [DEBUG] UPDATE EXECUTADO NO BANCO")


@receiver(post_save, sender=Capitulo)
def capitulo_salvo(sender, instance, created, **kwargs):
    print("🔥 [DEBUG] SIGNAL POST_SAVE CAPITULO EXECUTOU")
    print(f"🔥 Capítulo ID: {instance.id} | Criado: {created}")

    try:
        atualizar(instance.volume.anime)
    except Exception as e:
        print("❌ ERRO NO SIGNAL POST_SAVE:", e)


@receiver(post_delete, sender=Capitulo)
def capitulo_deletado(sender, instance, **kwargs):
    print("🔥 [DEBUG] SIGNAL POST_DELETE CAPITULO EXECUTOU")
    print(f"🔥 Capítulo deletado ID: {instance.id}")

    try:
        atualizar(instance.volume.anime)
    except Exception as e:
        print("❌ ERRO NO SIGNAL POST_DELETE:", e)


@receiver(post_save, sender=Capitulo)
def atualizar_anime_ao_salvar_capitulo(sender, instance, **kwargs):
    print("🔥 [DEBUG] ATUALIZANDO POSIÇÃO DE NOVO ANIME")
    anime = instance.volume.anime
    Anime.objects.filter(id=anime.id).update(atualizado_em=timezone.now())