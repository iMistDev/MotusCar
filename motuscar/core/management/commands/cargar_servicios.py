from django.core.management.base import BaseCommand
from core.models.mecanico import Mecanico
from core.models.servicio import Servicio
from datetime import timedelta

class Command(BaseCommand):
    help = 'Carga servicios por defecto según la especialidad de los mecánicos'

    def handle(self, *args, **kwargs):
        especialidades = {
            'lubricentro': [
                {'nombre': 'Cambio de aceite', 'precio': 20000, 'duracion': 30},
                {'nombre': 'Cambio de filtro de aire', 'precio': 10000, 'duracion': 20}
            ],
            'electrico': [
                {'nombre': 'Revisión de sistema eléctrico', 'precio': 25000, 'duracion': 45},
                {'nombre': 'Cambio de batería', 'precio': 30000, 'duracion': 30}
            ],
            'vulcanizacion': [
                {'nombre': 'Parche de neumático', 'precio': 8000, 'duracion': 15},
                {'nombre': 'Cambio de neumático', 'precio': 15000, 'duracion': 30}
            ],
            'mecanica': [
                {'nombre': 'Revisión de frenos', 'precio': 25000, 'duracion': 40},
                {'nombre': 'Alineación y balanceo', 'precio': 30000, 'duracion': 60}
            ],
            'pintura': [
                {'nombre': 'Pintado de parachoques', 'precio': 50000, 'duracion': 120},
                {'nombre': 'Pintado completo', 'precio': 200000, 'duracion': 300}
            ],
        }

        for m in Mecanico.objects.all():
            clave = m.especialidad.strip().lower()
            if clave in especialidades:
                for s in especialidades[clave]:
                    servicio, creado = Servicio.objects.get_or_create(
                        nombre=s['nombre'],
                        defaults={
                            'precio': s['precio'],
                            'duracion_estimada': timedelta(minutes=s['duracion']),
                            'descripcion': ''
                        }
                    )
                    # Agregar el mecánico a la relación ManyToMany, si no está
                    if not servicio.mecanicos.filter(id=m.id).exists():
                        servicio.mecanicos.add(m)
                        self.stdout.write(f'Servicio "{s["nombre"]}" asignado a {m.nombre}')
                    elif creado:
                        self.stdout.write(f'Servicio "{s["nombre"]}" creado y asignado a {m.nombre}')

        self.stdout.write(self.style.SUCCESS('Servicios cargados correctamente.'))
