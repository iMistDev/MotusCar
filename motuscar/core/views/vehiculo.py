from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from safedelete import HARD_DELETE
from core.models.vehiculo import Vehiculo
from core.forms.vehiculo import VehiculoForm

def home(request):
    return render(request, 'index.html')

def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculo/listar.html', {'vehiculos': vehiculos, 'active': 'listar'})

def crear_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo creado exitosamente')
            return redirect('listar_vehiculos')
    else:
        form = VehiculoForm()
    return render(request, 'vehiculo/crear.html', {'form': form, 'active': 'crear'})

def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo.all_objects, pk=vehiculo_id)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado exitosamente')
            return redirect('listar_vehiculos')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'vehiculo/editar.html', {'form': form, 'active': 'editar'})

def vehiculos_eliminados(request):
    vehiculos = Vehiculo.deleted_objects.all()
    return render(request, 'vehiculo/eliminados.html', {'vehiculos': vehiculos})

def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo.objects.all(), pk=vehiculo_id)
    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, f'Vehículo {vehiculo.patente} enviado a papelera')
        return redirect('listar_vehiculos')
    return render(request, 'vehiculo/eliminar.html', {'vehiculo': vehiculo, 'active': 'eliminar'})

def restaurar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo.all_objects.filter(deleted__isnull=False), pk=vehiculo_id)
    vehiculo.deleted = None
    vehiculo.save()
    messages.success(request, f'Vehículo {vehiculo.patente} restaurado')
    return redirect('listar_vehiculos')

def eliminar_definitivamente(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo.deleted_objects, pk=vehiculo_id)
    if request.method == 'POST':
        vehiculo.delete(force_policy=HARD_DELETE)
        messages.success(request, f'Vehículo {vehiculo.patente} eliminado permanentemente')
        return redirect('listar_vehiculos')
    return render(request, 'vehiculo/eliminar_definitivo.html', {'vehiculo': vehiculo})