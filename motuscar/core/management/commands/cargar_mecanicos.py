from django.core.management.base import BaseCommand
from core.models import Mecanico, Servicio, DisponibilidadMecanico
from datetime import time, timedelta
from django.core.validators import EmailValidator

class Command(BaseCommand):
    help = 'Carga datos de prueba completos para mecánicos, servicios y disponibilidad'

    def handle(self, *args, **options):
        # === 1. Crear Mecánicos ===
        mecanicos_data = [
<<<<<<< HEAD
            {"nombre": "Juan", "apellido": "Pérez", "email": "juan.perez@example.com", "region": "Biobío", "comuna": "Concepción", "direccion": "Av. Collao 1234", "especialidad": "lubricentro", "tipo": "taller"},
            {"nombre": "Pedro", "apellido": "López", "email": "pedro.lopez@example.com", "region": "Biobío", "comuna": "Concepción", "direccion": "O'Higgins 1122", "especialidad": "electrico", "tipo": "taller"},
            {"nombre": "Luis", "apellido": "Torres", "email": "luis.torres@example.com", "region": "Biobío", "comuna": "Concepción", "direccion": "Av. Paicaví 456", "especialidad": "vulcanizacion", "tipo": "taller"},
            {"nombre": "Héctor", "apellido": "Vargas", "email": "hector.vargas@example.com", "region": "Biobío", "comuna": "Concepción", "direccion": "Av. Chacabuco 789", "especialidad": "mecanica", "tipo": "taller"},
            {"nombre": "Arturo", "apellido": "Miranda", "email": "arturo.miranda@example.com", "region": "Biobío", "comuna": "Concepción", "direccion": "Av. Los Robles 667", "especialidad": "pintura", "tipo": "taller"},
=======
            {"nombre": "Juan", "apellido": "Pérez", "email": "juan.perez@example.com", "region": "biobio", "comuna": "Talcahuano", "direccion": "Av. Collao 1234", "especialidad": "lubricentro", "tipo": "taller"},
            {"nombre": "Pedro", "apellido": "López", "email": "pedro.lopez@example.com", "region": "biobio", "comuna": "Chiguayante", "direccion": "O'Higgins 1122", "especialidad": "electrico", "tipo": "taller"},
            {"nombre": "Luis", "apellido": "Torres", "email": "luis.torres@example.com", "region": "biobio", "comuna": "Concepción", "direccion": "Av. Paicaví 456", "especialidad": "vulcanizacion", "tipo": "taller"},
            {"nombre": "Héctor", "apellido": "Vargas", "email": "hector.vargas@example.com", "region": "biobio", "comuna": "Concepción", "direccion": "Av. Chacabuco 789", "especialidad": "mecanica", "tipo": "taller"},
            {"nombre": "Arturo", "apellido": "Miranda", "email": "arturo.miranda@example.com", "region": "biobio", "comuna": "Concepción", "direccion": "Av. Los Robles 667", "especialidad": "pintura", "tipo": "taller"},
>>>>>>> Develop
        ]

        mecanicos = []
        for data in mecanicos_data:
            m, created = Mecanico.objects.get_or_create(email=data['email'], defaults=data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Mecánico creado: {m}"))
            mecanicos.append(m)

        # === 2. Crear Servicios y Asignar ===
        servicios_por_especialidad = {
            'lubricentro': [
                {'nombre': 'Cambio de aceite', 'precio': 20000, 'duracion': 30},
                {'nombre': 'Cambio de filtro de aire', 'precio': 10000, 'duracion': 20}
            ],
            'electrico': [
                {'nombre': 'Revisión sistema eléctrico', 'precio': 25000, 'duracion': 45},
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

        for m in mecanicos:
            servicios = servicios_por_especialidad.get(m.especialidad, [])
            for s in servicios:
                servicio = Servicio.objects.create(
                    mecanicos=m,
                    nombre=s['nombre'],
                    precio=s['precio'],
                    duracion_estimada=timedelta(minutes=s['duracion'])
                )
                self.stdout.write(f"Servicio '{servicio.nombre}' creado para {m}")

        # === 3. Crear Disponibilidad Lunes a Viernes + Sábado ===
        disponibilidad = [
            (0, time(9, 0), time(18, 0)),  # Lunes
            (1, time(9, 0), time(18, 0)),
            (2, time(9, 0), time(18, 0)),
            (3, time(9, 0), time(18, 0)),
            (4, time(9, 0), time(18, 0)),
            (5, time(10, 0), time(14, 0)),  # Sábado
        ]

        for m in mecanicos:
            for dia, inicio, fin in disponibilidad:
                DisponibilidadMecanico.objects.get_or_create(
                    mecanico=m,
                    dia_semana=dia,
                    defaults={
                        'hora_inicio': inicio,
                        'hora_fin': fin,
                        'disponible': True
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Disponibilidad creada para {m}"))

        self.stdout.write(self.style.SUCCESS("Todos los datos de prueba fueron cargados correctamente."))