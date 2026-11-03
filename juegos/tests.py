import json

from django.test import TestCase
from django.urls import reverse

from .models import Nivel, Partida


class PantallasTests(TestCase):
    def setUp(self):
        self.nivel1 = Nivel.objects.create(numero=1, nombre="Patrulla", descripcion="Fácil", meta_puntos=50)
        self.nivel2 = Nivel.objects.create(numero=2, nombre="Meteoros", descripcion="Medio", meta_puntos=100,
                                           vidas=2, velocidad_enemigos=3.5, frames_entre_enemigos=40)

    def test_inicio_y_niveles(self):
        self.assertContains(self.client.get(reverse("juegos:inicio")), "Galaxy")
        respuesta = self.client.get(reverse("juegos:niveles"))
        self.assertContains(respuesta, "Patrulla")
        self.assertContains(respuesta, "Meteoros")

    def test_jugar_entrega_la_configuracion_y_los_scripts(self):
        respuesta = self.client.get(reverse("juegos:jugar", args=[2]))
        self.assertContains(respuesta, 'id="config-nivel"')
        self.assertContains(respuesta, 'id="juego"')
        self.assertContains(respuesta, "phaser.min.js")
        self.assertContains(respuesta, "galaxy/game.js")
        config = respuesta.context["config"]
        self.assertEqual(config["meta_puntos"], 100)
        self.assertEqual(config["vidas"], 2)
        self.assertEqual(config["velocidad_enemigos"], 3.5)
        self.assertEqual(config["url_resultado"], reverse("juegos:guardar_resultado", args=[2]))
        self.assertTrue(config["csrf"])

    def test_nivel_inexistente(self):
        self.assertEqual(self.client.get(reverse("juegos:jugar", args=[99])).status_code, 404)


class ResultadoTests(TestCase):
    def setUp(self):
        self.nivel1 = Nivel.objects.create(numero=1, nombre="Patrulla", descripcion="Fácil", meta_puntos=50)
        self.nivel2 = Nivel.objects.create(numero=2, nombre="Meteoros", descripcion="Medio", meta_puntos=100)
        self.url = reverse("juegos:guardar_resultado", args=[1])

    def enviar(self, datos):
        return self.client.post(self.url, data=json.dumps(datos), content_type="application/json")

    def test_guarda_victoria_y_redirige_a_ganaste(self):
        respuesta = self.enviar({"gano": True, "puntos": 60})
        self.assertEqual(respuesta.status_code, 200)
        partida = Partida.objects.get()
        self.assertTrue(partida.gano)
        self.assertIsNone(partida.jugador)
        self.assertEqual(respuesta.json()["redirect"], reverse("juegos:resultado", args=[partida.id]))
        pantalla = self.client.get(respuesta.json()["redirect"])
        self.assertContains(pantalla, "¡Ganaste!")
        self.assertContains(pantalla, "Nivel 2")

    def test_guarda_derrota_y_redirige_a_perdiste(self):
        respuesta = self.enviar({"gano": False, "puntos": 20})
        pantalla = self.client.get(respuesta.json()["redirect"])
        self.assertContains(pantalla, "Perdiste")
        self.assertContains(pantalla, "Reintentar")

    def test_datos_invalidos(self):
        for datos in ({"gano": "si", "puntos": 10}, {"gano": True, "puntos": "abc"}, {"gano": True},
                      {"gano": True, "puntos": -1}, {"gano": True, "puntos": True}):
            self.assertEqual(self.enviar(datos).status_code, 400, datos)
        self.assertEqual(Partida.objects.count(), 0)

    def test_solo_post(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_exige_token_csrf(self):
        from django.test import Client
        estricto = Client(enforce_csrf_checks=True)
        respuesta = estricto.post(self.url, data=json.dumps({"gano": True, "puntos": 10}), content_type="application/json")
        self.assertEqual(respuesta.status_code, 403)
