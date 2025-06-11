from django.core.management.base import BaseCommand
from core.models.disponibilidad import DisponibilidadMecanico
from core.models.mecanico import Mecanico
from datetime import time

class Command(BaseCommand):
    help = 'Carga horarios de disponibilidad por defecto para los mecánicos'

    def handle(self, *args, **options):
        #horario laboral 9-18 hrs
        horario_base = [
            (0, time(9, 0), time(18, 0)),  # Lunes
            (1, time(9, 0), time(18, 0)),  # Martes
            (2, time(9, 0), time(18, 0)),  # Miércoles
            (3, time(9, 0), time(18, 0)),  # Jueves
            (4, time(9, 0), time(18, 0)),  # Viernes
            (5, time(10, 0), time(14, 0)), # Sábado (medio día)
        ]

        for mecanico in Mecanico.objects.all():
            for dia, inicio, fin in horario_base:
                DisponibilidadMecanico.objects.get_or_create(
                    mecanico=mecanico,
                    dia_semana=dia,
                    defaults={
                        'hora_inicio': inicio,
                        'hora_fin': fin,
                        'disponible': True
                    }
                )
            self.stdout.write(self.style.SUCCESS(f'Disponibilidad creada para {mecanico}'))