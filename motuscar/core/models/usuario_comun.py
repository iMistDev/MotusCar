from django.db import models
from login.models import CustomUser

class UsuarioComun(CustomUser):
    #telefono = models.CharField(max_length=20, blank=True)
    
    #vehiculos = models.ManyToManyField('core.Vehiculo', blank=True)

    class Meta:
        db_table = 'usuario_comun'

    @property
    def es_mecanico(self):
        return False
    
    @property
    def es_usuario_comun(self):
        return True

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
