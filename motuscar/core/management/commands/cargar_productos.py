from django.core.management.base import BaseCommand
from core.models import Products  # Ajusta la importación según tu estructura
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Carga datos de prueba para productos de repuestos'

    def handle(self, *args, **options):
        productos_data = [
            {
                "Nombre_Producto": "Filtro de Aceite",
                "Código_SKU": "FO-001",
                "Proveedor": "Repuestos Premium",
                "Categoria": "Motor",
                "Precio_Unitario": 24990,
                "Cantidad": 15,
                "Descripcion": "Filtro de aceite de alta calidad para todo tipo de vehículos"
            },
            {
                "Nombre_Producto": "Pastillas de Freno",
                "Código_SKU": "PF-002",
                "Proveedor": "Frenos y Más",
                "Categoria": "Frenos",
                "Precio_Unitario": 45500,
                "Cantidad": 8,
                "Descripcion": "Pastillas de freno cerámicas, mayor durabilidad"
            },
            {
                "Nombre_Producto": "Kit de Embrague",
                "Código_SKU": "KE-003",
                "Proveedor": "Transmisiones XYZ",
                "Categoria": "Transmisión",
                "Precio_Unitario": 120000,
                "Cantidad": 5,
                "Descripcion": "Kit completo de embrague para transmisión manual"
            },
            {
                "Nombre_Producto": "Amortiguadores Delanteros",
                "Código_SKU": "AM-004",
                "Proveedor": "Suspensiones Premium",
                "Categoria": "Suspensión",
                "Precio_Unitario": 85750,
                "Cantidad": 3,
                "Descripcion": "Amortiguadores delanteros de alta resistencia"
            },
            {
                "Nombre_Producto": "Batería 12V 60Ah",
                "Código_SKU": "BT-005",
                "Proveedor": "Energía Total",
                "Categoria": "Eléctrico",
                "Precio_Unitario": 89990,
                "Cantidad": 10,
                "Descripcion": "Batería de 12 voltios y 60 amperios por hora"
            },
            {
                "Nombre_Producto": "Correa de Distribución",
                "Código_SKU": "CD-006",
                "Proveedor": "Repuestos Premium",
                "Categoria": "Motor",
                "Precio_Unitario": 65250,
                "Cantidad": 7,
                "Descripcion": "Correa de distribución de alta durabilidad"
            },
            {
                "Nombre_Producto": "Aceite Motor 5W-30",
                "Código_SKU": "AM-007",
                "Proveedor": "Lubricantes Premium",
                "Categoria": "Motor",
                "Precio_Unitario": 18990,
                "Cantidad": 20,
                "Descripcion": "Aceite sintético 5W-30 para motor, 5 litros"
            },
            {
                "Nombre_Producto": "Bujías de Encendido",
                "Código_SKU": "BE-008",
                "Proveedor": "Sistema Eléctrico Total",
                "Categoria": "Motor",
                "Precio_Unitario": 12990,
                "Cantidad": 12,
                "Descripcion": "Bujías de iridio para mejor rendimiento"
            },
            {
                "Nombre_Producto": "Radiador",
                "Código_SKU": "RD-009",
                "Proveedor": "Cooling Systems",
                "Categoria": "Motor",
                "Precio_Unitario": 115000,
                "Cantidad": 4,
                "Descripcion": "Radiador de aluminio para sistema de refrigeración"
            },
            {
                "Nombre_Producto": "Discos de Freno",
                "Código_SKU": "DF-010",
                "Proveedor": "Frenos y Más",
                "Categoria": "Frenos",
                "Precio_Unitario": 75900,
                "Cantidad": 6,
                "Descripcion": "Discos de freno ventilados delanteros"
            }
        ]

        # Crear productos adicionales variados
        categorias = ["Motor", "Frenos", "Transmisión", "Suspensión", "Eléctrico"]
        proveedores = ["Repuestos Premium", "Frenos y Más", "Transmisiones XYZ", 
                      "Suspensiones Premium", "Energía Total", "Lubricantes Premium"]
        
        productos_extra = []
        for i in range(11, 31):  # 20 productos adicionales
            categoria = random.choice(categorias)
            proveedor = random.choice(proveedores)
            
            producto = {
                "Nombre_Producto": f"Producto {categoria} {i}",
                "Código_SKU": f"SKU-{i:03d}",
                "Proveedor": proveedor,
                "Categoria": categoria,
                "Precio_Unitario": random.randint(10000, 150000),
                "Cantidad": random.randint(1, 25),
                "Descripcion": f"Descripción del producto {categoria} {i} de {proveedor}"
                "Imagen_URL": f"https://picsum.photos/seed/{i}/400/400"
            }
            productos_extra.append(producto)
        
        # Combinar todos los productos
        todos_los_productos = productos_data + productos_extra
        
        # Contadores para estadísticas
        creados = 0
        actualizados = 0
        
        for producto_data in todos_los_productos:
            # Verificar si el producto ya existe por SKU
            sku = producto_data["Código_SKU"]
            
            imagen_url = producto_data.pop("Imagen_URL", none)
            try:
                producto = Products.objects.get(Código_SKU=sku)
                # Actualizar producto existente
                for key, value in producto_data.items():
                    setattr(producto, key, value)
                producto.save()
                actualizados += 1
                self.stdout.write(
                    self.style.WARNING(f'Producto actualizado: {producto.Nombre_Producto} | Imagen: {imagen_url}')
                )
            except Products.DoesNotExist:
                # Crear nuevo producto
                producto = Products.objects.create(**producto_data)
                creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Producto creado: {producto.Nombre_Producto} | Imagen: {imagen_url}')
                )
        
        # Mostrar resumen
        self.stdout.write(
            self.style.SUCCESS(
                f'\nProceso completado: {creados} productos creados, {actualizados} productos actualizados'
            )
        )