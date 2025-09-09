from django.db import models
from core.models.proveedor import Proveedor

class Products(models.Model):
    id_producto = models.AutoField(primary_key=True)
    Nombre_Producto = models.CharField(max_length=50)
    Código_SKU = models.CharField(max_length=50, verbose_name='Código SKU', unique=True)
    Proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    Categoria = models.CharField(max_length=100)
    Precio_Unitario = models.PositiveIntegerField(default=0)
    Descripcion = models.CharField(max_length=200)
    Fecha_Ingreso = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.Nombre_Producto} ({self.Código_SKU})"
    
    @property
    def stock_total(self):
        from core.models.inventario import Inventario  # Import local aquí
        return sum(inv.cantidad for inv in self.inventario.all())
    
    def stock_en_sucursal(self, sucursal):
        from core.models.inventario import Inventario  # Import local aquí
        try:
            return self.inventario.get(sucursal=sucursal).cantidad
        except Inventario.DoesNotExist:
            return 0