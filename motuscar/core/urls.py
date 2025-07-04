# core/urls.py
from django.urls import path

#URL Productos
from core.views.inventario import listar_productos, crear_productos, editar_producto, eliminar_producto

#URL Vehículos
from core.views.vehiculo import (
    listar_vehiculos, crear_vehiculo, editar_vehiculo,
    eliminar_vehiculo, vehiculos_eliminados, restaurar_vehiculo, eliminar_definitivamente
)

#URL Usuarios
from core.views.usuarios import user_list, user_manage, UserDeleteView

#URL Mecanico
from core.views.mecanico import listar_mecanico, crear_mecanico, editar_mecanico, eliminar_mecanico, asignar_servicios_disponibilidad
from core.views.mecanico import listar_mecanico, crear_mecanico, editar_mecanico, eliminar_mecanico, asignar_servicios_disponibilidad

#URL Agenda
from core.views.agenda import (
    cambiar_estado_agenda, listar_mecanicos, editar_agenda, eliminar_agenda, horarios_ocupados, listar_mecanicos,
    agendar_cita, listar_agenda
)

#URL USUARIO COMUN
from core.views.usuario_comun import listar_usuario_comun, crear_usuario_comun, editar_usuario_comun, EliminarUsuarioComun

 

urlpatterns = [
    #URL Vehículos
    path('vehiculos/', listar_vehiculos, name='listar_vehiculos'),
    path('vehiculos/crear/', crear_vehiculo, name='crear_vehiculo'),
    path('vehiculos/editar/<int:vehiculo_id>/', editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', eliminar_vehiculo, name='eliminar_vehiculo'),
    path('vehiculos/eliminados/', vehiculos_eliminados, name='vehiculos_eliminados'),
    path('vehiculos/restaurar/<int:vehiculo_id>/', restaurar_vehiculo, name='restaurar_vehiculo'),
    path('vehiculos/eliminar-definitivo/<int:vehiculo_id>/', eliminar_definitivamente, name='eliminar_definitivo'),

    #URL Usuarios
    path('usuarios/', user_list, name='user_list'),
    path('usuarios/create/', user_manage, name='user_create'),
    path('usuarios/<int:pk>/edit/', user_manage, name='user_update'),
    path('usuarios/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    
    #URL Productos
    path('productos/', listar_productos, name='listar_productos'),
    path('productos/crear/', crear_productos, name='crear_producto'),
    path('productos/editar/<int:id>', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>', eliminar_producto, name='eliminar_producto'),
    
    #URL Mecanico
    path('mecanico/', listar_mecanico, name='listar_mecanico'),
    path('mecanico/crear/', crear_mecanico, name='crear_mecanico'),
    path('mecanico/<int:mecanico_id>/editar/', editar_mecanico, name='editar_mecanico'),
    path('mecanico/<int:mecanico_id>/eliminar/', eliminar_mecanico, name='eliminar_mecanico'),
    path('mecanico/<int:mecanico_id>/asignar/', asignar_servicios_disponibilidad, name='asignar_servicios_disponibilidad'),

    #URL Agenda
    path('agenda/', listar_agenda, name='listar_agenda'),
    path('agenda/editar/<int:agenda_id>/', editar_agenda, name='editar_agenda'),
    path('agenda/eliminar/<int:agenda_id>/', eliminar_agenda, name='eliminar_agenda'),
    path('agenda/horarios_ocupados/', horarios_ocupados, name='horarios_ocupados'), 
    path('agenda/estado/<int:agenda_id>/', cambiar_estado_agenda, name='cambiar_estado_agenda'),

    
    #URL Agenda -> Buscar mecanico
    path('agenda/mecanico/', listar_mecanicos, name='listar_mecanicos'),
    path('agenda/mecanico/<int:mecanico_id>/servicio/<int:servicio_id>/agendar/', agendar_cita, name='agendar_cita'),

    #URL USUARIO COMUN
    path('usuario_comun/', listar_usuario_comun, name='listar_usuario_comun'),
    path('usuario_comun/crear/', crear_usuario_comun, name='crear_usuario_comun'),
    path('usuario_comun/<int:pk>/editar/', editar_usuario_comun, name='editar_usuario_comun'),
    path('usuario_comun/<int:pk>/eliminar/', EliminarUsuarioComun.as_view(), name='eliminar_usuario_comun'),
    
]