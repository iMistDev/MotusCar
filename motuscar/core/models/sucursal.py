from django.db import models

from core.constants.regiones import REGIONES_CHILE
from core.models.proveedor import Proveedor

class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    region = models.CharField(max_length=50, choices=REGIONES_CHILE)
    comuna = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='sucursales')
    
    def __str__(self):
        return f"{self.nombre} - {self.proveedor.nombre}"