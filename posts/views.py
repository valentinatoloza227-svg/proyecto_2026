from django.shortcuts import render, get_object_or_404, redirect

from .models import Post

from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "posts/index.html")


def lista_posts(request):
    posts = Post.objects.filter(activo=True).order_by("-publicado")
    return render(request, "posts/lista.html", {"posts": posts})

def detalle_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/detalle.html", {"post": post})

#@login_required
def crear_post(request):
    if request.method == 'POST':
        titulo    = request.POST['titulo']
        contenido = request.POST['contenido']
        Post.objects.create(titulo=titulo, contenido=contenido,autor=request.user)
        return redirect("lista_posts")
    return render(request, "posts/crear.html")


