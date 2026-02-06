from django.contrib import admin
from .models import Venditore, Cliente

# Register your models here.


admin.site.register(Cliente)
admin.site.register(Venditore)