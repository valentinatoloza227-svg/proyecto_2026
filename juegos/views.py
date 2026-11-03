import json

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Nivel, Partida


def inicio(request):
    return render(request, "juegos/inicio.html")


def niveles(request):
    return render(request, "juegos/niveles.html", {"niveles": Nivel.objects.all()})


def jugar(request, numero):
    nivel = get_object_or_404(Nivel, numero=numero)
    # La configuración que Django le entrega al juego (la plantilla la convierte en JSON).
    config = {
        "numero": nivel.numero,
        "nombre": nivel.nombre,
        "meta_puntos": nivel.meta_puntos,
        "vidas": nivel.vidas,
        "velocidad_enemigos": nivel.velocidad_enemigos,
        "frames_entre_enemigos": nivel.frames_entre_enemigos,
        "url_resultado": reverse("juegos:guardar_resultado", args=[nivel.numero]),
        "csrf": get_token(request),
    }
    return render(request, "juegos/jugar.html", {"nivel": nivel, "config": config})


@require_POST
def guardar_resultado(request, numero):
    nivel = get_object_or_404(Nivel, numero=numero)
    # TODO 5: leer el resultado que manda el juego, validarlo, guardar la partida y responder con la pantalla a la que hay que ir.


def resultado(request, partida_id):
    partida = get_object_or_404(Partida.objects.select_related("nivel"), id=partida_id)
    siguiente = Nivel.objects.filter(numero__gt=partida.nivel.numero).first()
    plantilla = "juegos/ganaste.html" if partida.gano else "juegos/perdiste.html"
    return render(request, plantilla, {"partida": partida, "siguiente": siguiente})
