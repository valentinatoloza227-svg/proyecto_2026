from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='juego_inicio'),
    path('personajes/', views.personajes, name='juego_personajes'),
    path('niveles/', views.niveles, name='juego_niveles'),
    path('controles/', views.controles, name='juego_controles'),
    path('creditos/', views.creditos, name='juego_creditos'),
]
