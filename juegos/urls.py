from django.urls import path

from . import views

app_name = "juegos"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("niveles/", views.niveles, name="niveles"),
    path("jugar/<int:numero>/", views.jugar, name="jugar"),
    path("jugar/<int:numero>/resultado/", views.guardar_resultado, name="guardar_resultado"),
    path("resultado/<int:partida_id>/", views.resultado, name="resultado"),
]
