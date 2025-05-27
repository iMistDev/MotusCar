#admin.py es para configurar la url /admin

from django.contrib import admin

#al dejarlos asi (de forma basica), funciona como crud
#se puede editar para mejorar la vista y opciones

from core.models.vehiculo import Vehiculo
admin.site.register(Vehiculo)

from core.models.inventario import Products
admin.site.register(Products)

from core.models.usuarios import Usuario
admin.site.register(Usuario)