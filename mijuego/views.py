from django.shortcuts import render

# Create your views here.

from django.shortcuts import render


def inicio(request):
    return render(request, 'mijuego/inicio.html')


def personajes(request):
    return render(request, 'mijuego/personajes.html')


def niveles(request):
    return render(request, 'mijuego/niveles.html')


def controles(request):
    return render(request, 'mijuego/controles.html')

def creditos(request):
    return render(request, 'mijuego/creditos.html')