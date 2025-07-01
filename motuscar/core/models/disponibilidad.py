from django.db import models
from django.core.exceptions import ValidationError
from datetime import time

class DisponibilidadMecanico(models.Model):
    mecanico = models.ForeignKey('core.Mecanico', on_delete=models.CASCADE, null=True, blank=True)
    dia_semana = models.PositiveSmallIntegerField(choices=[
        (0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'), 
        (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo')
    ])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    disponible = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'disponibilidad_mecanico'
        verbose_name_plural = 'Disponibilidades de Mecánicos'
        unique_together = ('mecanico', 'dia_semana')

    def clean(self):
        if self.hora_inicio >= self.hora_fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin")
    
    def __str__(self):
        return f"{self.mecanico} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"