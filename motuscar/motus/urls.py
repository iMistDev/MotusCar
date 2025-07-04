from django.urls import path, include  # Asegúrate de importar include
from . import views

urlpatterns = [
    path('', views.motus, name='motus'),
    path('core/', include('core.urls')),
]
