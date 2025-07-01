from django.db import models
from django.core.validators import EmailValidator

from core.constants.regiones import REGIONES_CHILE
from core.constants.servicios import ESPECIALIDAD, TIPOS

class Mecanico(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(validators=[EmailValidator()], unique=True)
    region = models.CharField(max_length=50, choices=REGIONES_CHILE)
    comuna = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    especialidad = models.CharField(max_length=50, choices=ESPECIALIDAD)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    servicios = models.ManyToManyField('core.Servicio', blank=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.especialidad} ({self.comuna})'

    class Meta:
        db_table = 'mecanico'