from django.db import models
from django.utils.translation import gettext_lazy as _

from login.models import CustomUser

from core.constants.regiones import REGIONES_CHILE
from core.constants.servicios import ESPECIALIDAD, TIPOS

from django.contrib.auth import get_user_model
User = get_user_model()

class Mecanico(CustomUser):

    region = models.CharField(max_length=50, choices=REGIONES_CHILE)
    comuna = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    especialidad = models.CharField(max_length=50, choices=ESPECIALIDAD)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    servicios = models.ManyToManyField('core.Servicio', blank=True)

    class Meta:
        db_table = 'mecanico'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.especialidad} ({self.comuna})'
