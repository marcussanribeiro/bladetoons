from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from backend.model.model_anime import Capitulo

class Grupo(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
    


class UsuarioCustom(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)

    entidade = models.CharField(max_length=100, null=True, blank=True)
    vip = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Só criptografa se não estiver criptografada ainda
        if not self.senha.startswith('pbkdf2_'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def check_senha(self, raw_password):
        return check_password(raw_password, self.senha)

    def __str__(self):
        return self.username
    


class CapituloLido(models.Model):
    user = models.ForeignKey(UsuarioCustom, on_delete=models.CASCADE)
    capitulo = models.ForeignKey('Capitulo', on_delete=models.CASCADE)
    lido = models.BooleanField(default=False)
    data_leitura = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'capitulo')