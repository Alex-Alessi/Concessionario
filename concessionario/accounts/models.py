from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    utente = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente")
    telefono = models.CharField(max_length=20, unique=True, blank=False, null=False)
    indirizzo = models.CharField(max_length=100, blank=False, null=False)
    data_iscrizione = models.DateField(auto_now_add=True)
    newsletter = models.BooleanField(default=False)

    def __str__(self):
        return self.utente.username
    

class Venditore(models.Model):
    utente = models.OneToOneField(User, on_delete=models.CASCADE, related_name="venditore")
    matricola = models.CharField(max_length=10, unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.utente.username}, {self.matricola}"