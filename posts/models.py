from django.db import models

# Create your models here.
# posts/models.py
from django.contrib.auth.models import User
class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    publicado = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    def __str__(self):
       return self.titulo