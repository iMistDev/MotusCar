from django.db import models

# Create your models here.

class Products(models.Model):
    id_producto = models.AutoField(primary_key=True)
    Nombre_Producto = models.CharField(max_length=50)
    Código_SKU = models.CharField(max_length=50, verbose_name='Código SKU', unique=True)
    Proveedor = models.CharField(max_length=100)
    Categoria = models.CharField(max_length=100)
    Precio_Unitario = models.PositiveIntegerField(default=0)
    Cantidad = models.PositiveIntegerField(default=0)
    Descripcion = models.CharField(max_length=200)
    Fecha_Ingreso = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.Nombre_Producto, self.Código_SKU)