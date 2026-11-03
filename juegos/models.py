from django.conf import settings
from django.db import models


class Nivel(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=60)
    descripcion = models.TextField()
    meta_puntos = models.PositiveIntegerField(help_text="Puntos necesarios para ganar")
    vidas = models.PositiveIntegerField(default=3)
    velocidad_enemigos = models.FloatField(default=2.0, help_text="Píxeles que baja un enemigo en cada vuelta")
    frames_entre_enemigos = models.PositiveIntegerField(
        default=60, help_text="Cada cuántas vueltas aparece un enemigo (60 = uno por segundo)")

    class Meta:
        ordering = ["numero"]
        verbose_name_plural = "niveles"

    def __str__(self):
        return f"Nivel {self.numero}: {self.nombre}"


class Partida(models.Model):
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, related_name="partidas")
    jugador = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    puntos = models.PositiveIntegerField()
    gano = models.BooleanField()
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada"]

    def __str__(self):
        return f"{self.nivel} - {'ganó' if self.gano else 'perdió'} con {self.puntos}"
