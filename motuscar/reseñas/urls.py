from django.urls import path
from . import views

urlpatterns = [
    path('crear/<int:producto_id>/<int:orden_id>/', views.crear_reseña, name='crear_reseña'),
]
