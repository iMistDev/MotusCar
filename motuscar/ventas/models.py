from django.db import models
from core.models.productos import Products
from login.models import CustomUser

# ELIMINA ESTA CLASE DUPLICADA - Ya tienes Products en core
# class Producto(models.Model):
#     nombre = models.CharField(max_length=100)
#     precio = models.DecimalField(max_digits=10, decimal_places=2)
#     descripcion = models.TextField(blank=True)
#     stock = models.PositiveIntegerField(default=0)
#     imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
# 
#     def __str__(self):
#         return self.nombre

class Carrito(models.Model):
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito {self.id}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)
    producto = models.ForeignKey(Products, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    def subtotal(self):
        # CORRECCIÓN: Usar Precio_Unitario en vez de precio
        return self.producto.Precio_Unitario * self.cantidad
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.Nombre_Producto}"

class Orden(models.Model):
    creado = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
    ], default='pendiente')

    def __str__(self):
        return f"Orden {self.id}"