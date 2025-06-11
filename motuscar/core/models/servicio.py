from django.db import models
from django.core.validators import MaxValueValidator

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    mecanicos = models.ManyToManyField('core.Mecanico')
    precio = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999999999)],
        help_text="Precio en pesos (sin decimales)"
    )
    duracion_estimada = models.DurationField()
    descripcion = models.TextField(blank=True)

    class Meta:
        db_table = 'servicio'