from django.db import models
from django.contrib.auth.models import User




    

class Valoracion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
   
    puntuacion = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.taller.nombre} ({self.puntuacion})"
