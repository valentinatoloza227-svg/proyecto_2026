from django.contrib import admin

from .models import Nivel, Partida


@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ("numero", "nombre", "meta_puntos", "vidas", "velocidad_enemigos", "frames_entre_enemigos")


@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ("nivel", "jugador", "puntos", "gano", "creada")
    list_filter = ("nivel", "gano")
