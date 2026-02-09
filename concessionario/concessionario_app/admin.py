from django.contrib import admin
from .models import Auto, Preferito, Ordine, FotoAuto, RichiestaInfo, LogoMarca

# Register your models here.

class FotoAutoInline(admin.TabularInline):
    model = FotoAuto
    extra = 3  # Mostra 3 slot vuoti

class AutoAdmin(admin.ModelAdmin):
    inlines = [FotoAutoInline]

admin.site.register(Auto, AutoAdmin)
admin.site.register(Preferito)
admin.site.register(Ordine)
admin.site.register(FotoAuto)
admin.site.register(RichiestaInfo)
admin.site.register(LogoMarca)