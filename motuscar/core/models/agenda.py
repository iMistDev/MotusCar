from django.db import models
from django.core.exceptions import ValidationError

from core.models.disponibilidad import DisponibilidadMecanico
from core.models.usuario_comun import UsuarioComun

class Agenda(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('realizada', 'Realizada')
    ]
     
    mecanico = models.ForeignKey('core.Mecanico', on_delete=models.CASCADE, null=True, blank=True)
    servicio = models.ForeignKey('core.Servicio', on_delete=models.CASCADE, null=True, blank=True)
    vehiculo = models.ForeignKey('core.Vehiculo', on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    descripcion = models.TextField(blank=True)
    usuariocomun = models.ForeignKey('core.UsuarioComun', on_delete=models.CASCADE, null=True, blank=True)

    
    
    class Meta:
        db_table = 'agenda'
        
     #evita que un mismo mecanico tenga mas de una cita en la misma fecha y hora:
    unique_together = ('mecanico', 'fecha', 'hora_inicio')
    
    # FUNCION PARA AGENDAR CITA SEGUN MECANICO Y SU DISPONIBILIDAD
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # verifica que hora_fin > hora_inicio
        if self.hora_inicio >= self.hora_fin:
            raise ValidationError("La hora de fin debe ser posterior a la hora de inicio")

        # solo validar si ya se ha seleccionad mecanico y fecha
        if hasattr(self, 'mecanico') and hasattr(self, 'fecha'):
            # validar que fecha y hora no se solapen con otras citas del mismo mecanico
            citas_solapadas = Agenda.objects.filter(
                mecanico=self.mecanico,
                fecha=self.fecha,
                hora_inicio__lt=self.hora_fin,
                hora_fin__gt=self.hora_inicio
            ).exclude(id=self.id)  # excluir la propia cita al editar

            if citas_solapadas.exists():
                raise ValidationError("El horario se solapa con otra cita existente")

            # validar disponibilidad del mecanico
            dia_semana = self.fecha.weekday()
            disponible = DisponibilidadMecanico.objects.filter(
                mecanico=self.mecanico,
                dia_semana=dia_semana,
                disponible=True,
                hora_inicio__lte=self.hora_inicio,
                hora_fin__gte=self.hora_fin
            ).exists()

            if not disponible:
                raise ValidationError("El mecánico no está disponible en ese horario")
            
        if self.vehiculo and self.vehiculo.usuario != self.usuariocomun:
            raise ValidationError("El vehículo seleccionado no pertenece al usuario")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)