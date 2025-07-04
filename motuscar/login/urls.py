# mi_app/urls.py
from django.urls import path
from . import views
#from .views import ver_perfil, editar_perfil
from django.urls import include

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.perf_view, name='profile'),
    path('motus/', include('motus.urls')),  # Asegúrate de que 'motus' es el nombre correcto de tu app
    
    path('registro/mecanico/crear', views.datos_mecanico, name='datos_mecanico'),
    path('mecanico/<int:mecanico_id>/asignar-servicios/', views.asignar_servicios, name='asignar_servicios'),
    path('mis-vehiculos/', views.vista_vehiculos_usuario, name='mis_vehiculos'),
    path('mis-vehiculos/crear/', views.crear_vehiculo, name='crear_vehiculo'),
    path('mis-vehiculos/editar/<int:vehiculo_id>/',views.editar_vehiculo, name='editar_vehiculo')
]