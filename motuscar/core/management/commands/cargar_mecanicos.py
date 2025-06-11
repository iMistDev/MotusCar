from django.core.management.base import BaseCommand
from core.models.mecanico import Mecanico

class Command(BaseCommand):
    help = 'Carga los datos iniciales de mecánicos en la base de datos'

    def handle(self, *args, **options):
        mecanicos_data = [
            # Lubricentro
            {
                "nombre": "Juan",
                "apellido": "Pérez",
                "region": "Biobío",
                "comuna": "Concepción",
                "direccion": "Av. Collao 1234",
                "especialidad": "lubricentro",
                "tipo": "taller"
            },
            {
                "nombre": "Carlos",
                "apellido": "González",
                "region": "Biobío",
                "comuna": "Concepción",
                "direccion": "Barros Arana 567",
                "especialidad": "lubricentro",
                "tipo": "particular"
            },
            {
                "nombre": "Miguel",
                "apellido": "Soto",
                "region": "Biobío",
                "comuna": "Talcahuano",
                "direccion": "Av. Colón 890",
                "especialidad": "lubricentro",
                "tipo": "taller"
            },
            {
                "nombre": "Roberto",
                "apellido": "Martínez",
                "region": "Biobío",
                "comuna": "Talcahuano",
                "direccion": "Av. Gran Bretaña 345",
                "especialidad": "lubricentro",
                "tipo": "particular"
            },
            
            # Eléctrico
            {
                "nombre": "Pedro",
                "apellido": "López",
                "region": "Biobío",
                "comuna": "Concepción",
                "direccion": "O'Higgins 1122",
                "especialidad": "electrico",
                "tipo": "taller"
            },
            {
                "nombre": "Francisco",
                "apellido": "Rodríguez",
                "region": "Biobío",
                "comuna": "Concepción",
                "direccion": "San Martín 334",
                "especialidad": "electrico",
                "tipo": "particular"
            },
            {
                "nombre": "Andrés",
                "apellido": "Silva",
                "region": "Biobío",
                "comuna": "Talcahuano",
                "direccion": "Av. Manuel Blanco 667",
                "especialidad": "electrico",
                "tipo": "taller"
            },
            {
                "nombre": "Jorge",
                "apellido": "Fuentes",
                "region": "Biobío",
                "comuna": "Talcahuano",
                "direccion": "Av. Cristóbal Colón 778",
                "especialidad": "electrico",
                "tipo": "particular"
            },
            
            # Vulcanización
            {
                "nombre": "Luis",
                "apellido": "Torres",
                "region": "Biobío",
                "comuna": "Concepción",
                "direccion": "Av. Paicaví 456",
                "especialidad": "vulcanizacion",
                "tipo": "taller"
            },
            {
                "nombre": "Diego",
                "apellido": "Mendoza",
                "region": "Biobío",
                "comuna": "Concepción",
                "direccion": "Av. Pedro de Valdivia 223",
                "especialidad": "vulcanizacion",
                "tipo": "particular"
            },
            {
                "nombre": "Sergio",
                "apellido": "Castro",
                "region": "Biobío",
                "comuna": "Talcahuano",
                "direccion": "Av. Almirante Riveros 991",
                "especialidad": "vulcanizacion",
                "tipo": "taller"
            },
            {
                "nombre": "Fernando",
                "apellido": "Riquelme",
                "region": "Biobío",
                "comuna": "Talcahuano",
                "direccion": "Av. Jorge Montt 112",
                "especialidad": "vulcanizacion",
                "tipo": "particular"
            },
            
            # Mecánica General
            {
                "nombre": "Héctor",
                "apellido": "Vargas",
                "region": "Biobío",
                "comuna": "Concepción",
                "direccion": "Av. Chacabuco 789",
                "especialidad": "mecanica",
                "tipo": "taller"
            },
            {
                "nombre": "Ricardo",
                "apellido": "Navarro",
                "region": "Biobío",
                "comuna": "Concepción",
                "direccion": "Av. Los Carrera 445",
                "especialidad": "mecanica",
                "tipo": "particular"
            },
            {
                "nombre": "Patricio",
                "apellido": "Araya",
                "region": "Biobío",
                "comuna": "Talcahuano",
                "direccion": "Av. San Martín 556",
                "especialidad": "mecanica",
                "tipo": "taller"
            },
            {
                "nombre": "Mario",
                "apellido": "Espinoza",
                "region": "Biobío",
                "comuna": "Talcahuano",
                "direccion": "Av. La Marina 334",
                "especialidad": "mecanica",
                "tipo": "particular"
            },
            
            # Pintura
            {
                "nombre": "Arturo",
                "apellido": "Miranda",
                "region": "Biobío",
                "comuna": "Concepción",
                "direccion": "Av. Los Robles 667",
                "especialidad": "pintura",
                "tipo": "taller"
            },
            {
                "nombre": "Raúl",
                "apellido": "Contreras",
                "region": "Biobío",
                "comuna": "Concepción",
                "direccion": "Av. Los Notros 889",
                "especialidad": "pintura",
                "tipo": "particular"
            },
            {
                "nombre": "Daniel",
                "apellido": "Sepúlveda",
                "region": "Biobío",
                "comuna": "Talcahuano",
                "direccion": "Av. Las Golondrinas 112",
                "especialidad": "pintura",
                "tipo": "taller"
            },
            {
                "nombre": "José",
                "apellido": "Morales",
                "region": "Biobío",
                "comuna": "Talcahuano",
                "direccion": "Av. Las Garzas 334",
                "especialidad": "pintura",
                "tipo": "particular"
            }
        ]

        if Mecanico.objects.exists():
            self.stdout.write(self.style.WARNING('Ya existen mecánicos en la base de datos. No se cargarán datos iniciales.'))
            return

        created_count = 0
        for mecanico_data in mecanicos_data:
            Mecanico.objects.create(**mecanico_data)
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Se han creado {created_count} mecánicos exitosamente'))