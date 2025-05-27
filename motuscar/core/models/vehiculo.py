from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE
from safedelete import SOFT_DELETE, HARD_DELETE
from safedelete.managers import SafeDeleteAllManager

class DeletedOnlyManager(SafeDeleteAllManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted__isnull=False)

class Vehiculo(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    
    TIPO_VEHICULO = [
        ('auto', 'Automóvil'),
        ('camioneta', 'Camioneta'),
        ('moto', 'Motocicleta'),
        ('bus', 'Bus'),
        ('camion', 'Camión')
    ]
    
    TIPO_COMBUSTIBLE = [
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diésel'),
        ('electrico', 'Eléctrico'),
        ('hibrido', 'Híbrido')
    ]
    
    patente = models.CharField(max_length=10, unique=True)
    usuario = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.IntegerField()
    tipo_combustible = models.CharField(max_length=20, choices=TIPO_COMBUSTIBLE)
    nro_chasis = models.CharField(max_length=50, blank=True, null=True)
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPO_VEHICULO)

    deleted_objects = DeletedOnlyManager()
    
    class Meta:
        db_table = 'vehiculo'