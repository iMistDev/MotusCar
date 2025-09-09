from django.core.management.base import BaseCommand
from django.db import transaction
from core.models.proveedor import Proveedor
from core.models.sucursal import Sucursal
from core.models.productos import Products
from core.models.inventario import Inventario


class Command(BaseCommand):
    help = 'Carga datos de prueba deterministas exclusivamente en la región Biobío'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Iniciando carga de datos de prueba (Biobío)..."))

        with transaction.atomic():
            # -------- Proveedores --------
            proveedores_data = [
                {"nombre": "Repuestos Premium", "contacto": "Juan Pérez", "telefono": "987654321", "email": "premium@proveedores.cl"},
                {"nombre": "AutoPartes Express", "contacto": "María López", "telefono": "912345678", "email": "express@proveedores.cl"},
                {"nombre": "FullCar Repuestos", "contacto": "Carlos Díaz", "telefono": "998877665", "email": "fullcar@proveedores.cl"},
            ]

            proveedores = []
            for p in proveedores_data:
                prov, created = Proveedor.objects.update_or_create(
                    nombre=p["nombre"],
                    defaults={"contacto": p["contacto"], "telefono": p["telefono"], "email": p["email"]}
                )
                proveedores.append(prov)
                self.stdout.write(f"Proveedor: {prov.nombre} ({'creado' if created else 'actualizado'})")

            # -------- Sucursales (todas en Biobío) --------
            sucursales_base = [
                ("Sucursal Chiguayante", "Chiguayante"),
                ("Sucursal Concepción", "Concepción"),
                ("Sucursal Hualpén", "Hualpén"),
                ("Sucursal Talcahuano", "Talcahuano"),
            ]

            for prov in proveedores:
                for suc_name, comuna in sucursales_base:
                    nombre_sucursal = f"{suc_name} - {prov.nombre}"
                    suc, created = Sucursal.objects.update_or_create(
                        nombre=nombre_sucursal,
                        proveedor=prov,
                        defaults={
                            "region": "biobio",         # Código de región según REGIONES_CHILE
                            "comuna": comuna,
                            "direccion": "Av. Principal 123",
                            "telefono": prov.telefono,
                        }
                    )
                    self.stdout.write(f"  Sucursal: {suc.nombre} (comuna: {suc.comuna}) -> {'creada' if created else 'actualizada'}")

            # -------- Productos base --------
            productos_base = [
                {"nombre": "Filtro de Aceite", "sku": "MO-001", "categoria": "Motor", "precio": 24990, "descripcion": "Filtro de aceite estándar"},
                {"nombre": "Pastillas de Freno", "sku": "FR-001", "categoria": "Frenos", "precio": 34990, "descripcion": "Juego de pastillas delanteras"},
                {"nombre": "Kit de Embrague", "sku": "TR-001", "categoria": "Transmisión", "precio": 159990, "descripcion": "Kit de embrague completo"},
                {"nombre": "Amortiguador", "sku": "SU-001", "categoria": "Suspensión", "precio": 55990, "descripcion": "Amortiguador hidráulico"},
                {"nombre": "Batería 60Ah", "sku": "EL-001", "categoria": "Eléctrico", "precio": 79990, "descripcion": "Batería libre de mantención"},
            ]

            # Cantidades por comuna para comparar tiendas
            cantidades_por_comuna = {
                "Chiguayante": 12,
                "Concepción": 20,
                "Hualpén": 5,
                "Talcahuano": 15,
            }

            # Crear productos y asignar inventario a todas las sucursales del proveedor
            for prod in productos_base:
                for prov in proveedores:
                    # SKU único por proveedor
                    sku_full = f"{prod['sku']}-{prov.id_proveedor}"

                    producto, prod_created = Products.objects.update_or_create(
                        **{"Código_SKU": sku_full},
                        defaults={
                            "Nombre_Producto": prod["nombre"],
                            "Proveedor": prov,
                            "Categoria": prod["categoria"],
                            "Precio_Unitario": prod["precio"],
                            "Descripcion": prod["descripcion"],
                        }
                    )
                    self.stdout.write(f"Producto: {producto.Nombre_Producto} ({sku_full}) -> {'creado' if prod_created else 'actualizado'}")

                    # Asignar inventario en todas las sucursales del proveedor
                    sucursales_prov = Sucursal.objects.filter(proveedor=prov, region="biobio")
                    for suc in sucursales_prov:
                        cantidad = cantidades_por_comuna.get(suc.comuna, 10)
                        inv, inv_created = Inventario.objects.update_or_create(
                            producto=producto,
                            sucursal=suc,
                            defaults={
                                "cantidad": cantidad,
                                "ubicacion": "Estante A-1"
                            }
                        )
                        self.stdout.write(f"    Inventario en {suc.comuna}: {inv.cantidad} unidades -> {'creado' if inv_created else 'actualizado'}")

        self.stdout.write(self.style.SUCCESS("✅ Carga completa — datos en Biobío creados/actualizados correctamente."))
