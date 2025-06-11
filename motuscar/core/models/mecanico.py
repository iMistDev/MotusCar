from django.db import models

class Mecanico(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    especialidad = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20)
    servicios = models.ManyToManyField('core.Servicio')

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.especialidad} ({self.comuna})'

    class Meta:
        db_table = 'mecanico'