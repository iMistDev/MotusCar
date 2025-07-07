from django.db import models
<<<<<<< HEAD
from django.core.validators import EmailValidator

from core.constants.regiones import REGIONES_CHILE
from core.constants.servicios import ESPECIALIDAD, TIPOS

class Mecanico(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(validators=[EmailValidator()], unique=True)
=======
from django.utils.translation import gettext_lazy as _

from login.models import CustomUser

from core.constants.regiones import REGIONES_CHILE
from core.constants.servicios import ESPECIALIDAD, TIPOS

from django.contrib.auth import get_user_model
User = get_user_model()

class Mecanico(CustomUser):

>>>>>>> Develop
    region = models.CharField(max_length=50, choices=REGIONES_CHILE)
    comuna = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    especialidad = models.CharField(max_length=50, choices=ESPECIALIDAD)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    servicios = models.ManyToManyField('core.Servicio', blank=True)
<<<<<<< HEAD

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.especialidad} ({self.comuna})'
=======
>>>>>>> Develop

    class Meta:
        db_table = 'mecanico'
    @property
    def es_mecanico(self):
        return True
    
    @property
    def es_usuario_comun(self):
        return False

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.especialidad} ({self.comuna})'

