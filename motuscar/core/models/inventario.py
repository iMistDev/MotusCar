from django.db import models

from core.models.productos import Products
from core.models.sucursal import Sucursal

class Inventario(models.Model):
    producto = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='inventario')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    ubicacion = models.CharField(max_length=50, blank=True)  # Ej: "Estante A-12"
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['producto', 'sucursal']  # Evita duplicados
    
    def __str__(self):
        return f"{self.producto} - {self.sucursal}: {self.cantidad} unidades"