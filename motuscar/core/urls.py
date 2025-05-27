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
]