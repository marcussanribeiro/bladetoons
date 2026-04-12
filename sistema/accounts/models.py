from django.db import models
from django.contrib.auth.hashers import make_password, check_password

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