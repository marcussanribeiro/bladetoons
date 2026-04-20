from django.db import models
from django.db.models import Sum
from django.utils.text import slugify
from django.db.models import F
from backend.model.model_accounts import UsuarioCustom


class Genero(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Anime(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='animes/', null=True, blank=True)
    generos = models.ManyToManyField(Genero, related_name='animes', null=True)
    slug = models.SlugField(unique=True, blank=True)
    total_capitulos = models.PositiveIntegerField(default=0)
    atualizado_em = models.DateTimeField(auto_now_add=True)
    criado_em = models.DateTimeField(auto_now=True)

    def total_visualizacoes(self):
        return Capitulo.objects.filter(
            volume__anime=self
        ).aggregate(total=Sum('visualizacoes'))['total'] or 0
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)

        # ⚠️ GARANTE que criado_em nunca seja alterado manualmente
        if self.pk:
            self.criado_em = Anime.objects.get(pk=self.pk).criado_em

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    
    def atualizar_total_capitulos(anime):
        total = Capitulo.objects.filter(volume__anime=anime).count()

        Anime.objects.filter(id=anime.id).update(total_capitulos=total)


class Volume(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='volumes')
    numero = models.IntegerField()

    def __str__(self):
        return f"{self.anime.titulo} - Volume {self.numero}"


class Capitulo(models.Model):
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, related_name='capitulos')
    titulo = models.CharField(max_length=200)
    numero = models.IntegerField()
    pdf = models.FileField(upload_to='capitulos/')

    # 🔥 contador de visualização
    visualizacoes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.volume.anime.titulo} - Cap {self.numero}"
    

class CapituloLido(models.Model):
    user = models.ForeignKey(UsuarioCustom, on_delete=models.CASCADE)
    capitulo = models.ForeignKey('Capitulo', on_delete=models.CASCADE)
    lido = models.BooleanField(default=False)
    data_leitura = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'capitulo')