from django.db import models
from django.core.validators import MaxValueValidator

class Servicio(models.Model):
    mecanicos = models.ForeignKey('core.Mecanico', on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    precio = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999999999)],
        help_text="Precio en pesos (sin decimales)"
    )
    duracion_estimada = models.DurationField()

    class Meta:
        db_table = 'servicio'