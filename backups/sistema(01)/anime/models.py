from django.db import models

class Anime(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    genero = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='animes/', null=True, blank=True)
    pdf = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.titulo