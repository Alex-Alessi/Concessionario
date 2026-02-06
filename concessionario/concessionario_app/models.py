from django.db import models
from accounts.models import Venditore, Cliente
from django.core.validators import MinValueValidator

# Create your models here.

CATEGORIA_CHOICES = [
    ('suv', 'SUV'),
    ('berlina', 'Berlina'),
    ('station_wagon', 'Station Wagon'),
    ('coupe', 'Coupé'),
    ('monovolume', 'Monovolume'),
    ('fuoristrada', 'Fuoristrada'),
    ('cabrio', 'Cabrio'),
    ('pick_up', 'Pick-up')
]

CONDIZIONI_CHOICES = [
    ('nuova', 'Nuova'),
    ('usata', 'Usata'),
    ('km0', 'Chilometro Zero')
]

ALIMENTAZIONE_CHOICES = [
    ('benzina', 'Benzina'),
    ('diesel', 'Diesel'),
    ('elettrica', 'Elettrica'),
    ('ibrida', 'Ibrida'),
    ('gpl', 'GPL'),
    ('metano', 'Metano')
]

CAMBIO_CHOICES = [
    ('manuale', 'Manuale'),
    ('automatico', 'Automatico'),
    ('semi-automatico', 'Semi-automatico')
]

EMISSIONI_CHOICES = [
    ('euro6d', 'Euro 6d'),
    ('euro6', 'Euro 6'),
    ('euro5', 'Euro 5'),
    ('euro4', 'Euro 4'),
    ('euro3', 'Euro 3')
]

STATO_CHOICES = [
    ('in_attesa_pagamento', 'In attesa pagamento'),
    ('pagato', 'Pagato'),
    ('in_consegna', 'In consegna'),
    ('consegnato', 'Consegnato'),
    ('annullato', 'Annullato')
]

METODO_CHOICES = [
    ('carta_di_credito', 'Carta di credito'),
    ('bonifico_bancario', 'Bonifico bancario'),
    ('leasing', 'Leasing'),
    ('pagamento_fisico', 'Pagamento fisico')
]

class Auto(models.Model):
    marca = models.CharField(max_length=50)
    video = models.FileField(upload_to='auto/video/', blank=True, null=True)
    modello = models.CharField(max_length=50)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    immatricolazione = models.DateField()
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    condizioni = models.CharField(max_length=5, choices=CONDIZIONI_CHOICES)
    alimentazione = models.CharField(max_length=9, choices=ALIMENTAZIONE_CHOICES)
    chilometraggio = models.IntegerField()
    tipo_cambio = models.CharField(max_length=15, choices=CAMBIO_CHOICES)
    potenza = models.CharField(max_length=50)
    classe_emissioni = models.CharField(max_length=6, choices=EMISSIONI_CHOICES)
    numero_porte = models.IntegerField()
    posti = models.IntegerField()
    sensori_parcheggio = models.BooleanField(default=False)
    cruise_control = models.BooleanField(default=False)
    frenata_emergenza = models.BooleanField(default=False)
    start_and_stop = models.BooleanField(default=False)
    incidenti_precedenti = models.BooleanField(default=False)
    disponibilita = models.BooleanField(default=True)
    luogo_veicolo = models.CharField(max_length=50)
    descrizione = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(Venditore, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.marca} {self.modello}"
    
class FotoAuto(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='foto_set')
    foto = models.ImageField(upload_to='auto/foto/')
    is_principale = models.BooleanField(default=False)  # Foto di copertina
    ordine = models.IntegerField(default=0)  # Per ordinare le foto
    caricata_il = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_principale', 'ordine']  # Principale prima, poi per ordine
        
    def __str__(self):
        return f"Foto di {self.auto}"
    
class RichiestaInfo(models.Model):
    auto = models.ForeignKey('Auto', on_delete=models.CASCADE, related_name='richieste')
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    messaggio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    gestita = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.auto}"


class Preferito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    data_creazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cliente', 'auto']

    def __str__(self):
        return f"{self.cliente} {self.auto}"
    
class Ordine(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    data_acquisto = models.DateTimeField(auto_now_add=True)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stato_ordine = models.CharField(max_length=19, choices=STATO_CHOICES, default='in_attesa_pagamento')
    pagamento = models.CharField(max_length=17, choices=METODO_CHOICES)
    indirizzo_consegna = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.cliente} {self.auto}"
