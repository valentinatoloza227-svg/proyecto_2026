from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="inicio"),
    path("posts/", views.lista_posts, name="lista_posts"),
    path("post/<int:pk>/", views.detalle_post, name="detalle_post"),
    path("crear/", views.crear_post, name="crear_post"),
]