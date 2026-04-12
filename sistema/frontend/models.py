from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

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