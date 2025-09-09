from django.db import models
from django.conf import settings
from core.models.productos import Products
from ventas.models import Orden
from login.models import CustomUser

class Reseña(models.Model):
    producto = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reseñas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reseñas')
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='reseñas')
    calificacion = models.PositiveSmallIntegerField(default=5)  # 1 a 5 estrellas
    comentario = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('producto', 'usuario', 'orden')  # Solo una reseña por compra

    def __str__(self):
        return f"{self.usuario} - {self.producto} ({self.calificacion}⭐)"
