from django.shortcuts import render, get_object_or_404, redirect
from core.forms.mecanico import MecanicoForm 
from django.contrib import messages

# Modelos
from core.models.mecanico import Mecanico
from core.models.servicio import Servicio
from core.models.disponibilidad import DisponibilidadMecanico

from datetime import time, timedelta
import importlib
import json

from core.constants.regiones import COMUNAS_POR_REGION, REGIONES_CHILE

from core.constants.servicios import SERVICIOS_POR_ESPECIALIDAD

servicios_por_especialidad = importlib.import_module("core.constants.servicios").SERVICIOS_POR_ESPECIALIDAD

DIA_SEMANA_CHOICES = [
    (0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'), 
    (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo')
]

TIPOS = ['taller', 'particular']
ESPECIALIDADES = ['lubricentro', 'electrico', 'vulcanizacion', 'mecanica', 'pintura']

def listar_mecanico(request):
    mecanicos = Mecanico.objects.all()
    return render(request, 'mecanico/listar.html', {
        'mecanicos': mecanicos,
        'regiones': REGIONES_CHILE,
        'comunas_por_region_json': json.dumps(COMUNAS_POR_REGION), 
        'tipos': TIPOS,
        'especialidades': ESPECIALIDADES,
        'active': 'mecanicos'
    })

def crear_mecanico(request):
    if request.method == 'POST':
        form = MecanicoForm(request.POST)
        if form.is_valid():
            mecanico = form.save()
            messages.success(request, 'Mecánico creado correctamente.')
            return redirect('asignar_servicios_disponibilidad', mecanico_id=mecanico.id)
        else:
            # recorrer errores de cada campo y agregarlos como mensajes
            for field, errors in form.errors.items():
                for error in errors:
                    verbose_field = form.fields[field].label if field in form.fields else field
                    messages.error(request, f"{verbose_field}: {error}")
    else:
        form = MecanicoForm()

    context = {
        'form': form,
        'comunas_por_region_json': json.dumps(COMUNAS_POR_REGION),
        'active': 'mecanicos'
    }
    return render(request, 'mecanico/crear.html', context)

def editar_mecanico(request, mecanico_id):
    mecanico = get_object_or_404(Mecanico, pk=mecanico_id)
    form = MecanicoForm(request.POST or None, instance=mecanico)

    if request.method == 'POST':
        # guardar mecanico
        if form.is_valid():
            form.save()

            messages.success(request, 'Mecánico actualizado.')
            return redirect('asignar_servicios_disponibilidad', mecanico_id=mecanico.id)

    return render(request, 'mecanico/editar.html', {
        'form': form,
        'mecanico': mecanico,
        'regiones': REGIONES_CHILE,
        'comunas_por_region_json': json.dumps(COMUNAS_POR_REGION),
        'active': 'mecanicos'
    })

def eliminar_mecanico(request, mecanico_id):
    mecanico = get_object_or_404(Mecanico, pk=mecanico_id)
    if request.method == 'POST':
        mecanico.delete()
        messages.success(request, 'Mecánico eliminado.')
        return redirect('listar_mecanico')
    return render(request, 'mecanico/eliminar.html', {'mecanico': mecanico, 'active': 'mecanicos'})

def asignar_servicios_disponibilidad(request, mecanico_id):
    mecanico = get_object_or_404(Mecanico, id=mecanico_id)
    duraciones = [30, 45, 60, 90, 120]

    if request.method == 'POST':
        DisponibilidadMecanico.objects.filter(mecanico=mecanico).delete()
        Servicio.objects.filter(mecanicos=mecanico).delete()
        #DEJAR EN 'MECANICOS', MODELS SERVICIO USA MECANICOS NO MECANICO
        
        servicios_seleccionados = request.POST.getlist('servicios')  # lista de forloop.counter (indices)

        for idx in servicios_seleccionados:
            nombre = request.POST.get(f'nombre_{idx}', '')
            precio = request.POST.get(f'precio_{idx}', '0')
            duracion_str = request.POST.get(f'duracion_{idx}', '')

            try:
                h, m, _ = map(int, duracion_str.split(':'))  # HH:MM:SS
                duracion = timedelta(hours=h, minutes=m)
            except:
                duracion = timedelta(minutes=30)

            if not nombre or not precio or not duracion_str:
                messages.error(request, f"Falta algún dato para el servicio seleccionado ({nombre}).")
                return redirect('asignar_servicios_disponibilidad', mecanico_id=mecanico_id)

            Servicio.objects.create(
                mecanicos=mecanico,
                nombre=nombre,
                precio=precio,
                duracion_estimada=duracion
            )

        #doble check eliminar la dispon. anterior
        DisponibilidadMecanico.objects.filter(mecanico=mecanico).delete()
        # Obtener horario general (lunes a viernes)
        hora_inicio_general = request.POST.get('hora_inicio_general')
        hora_fin_general = request.POST.get('hora_fin_general')

        # aplicar disponibilidad de lunes (0) a viernes (4)
        if hora_inicio_general and hora_fin_general:
            hora_inicio = time.fromisoformat(hora_inicio_general)
            hora_fin = time.fromisoformat(hora_fin_general)
            if hora_inicio < hora_fin:
                for dia in range(0, 5):  # lunes a viernes
                    DisponibilidadMecanico.objects.create(
                        mecanico=mecanico,
                        dia_semana=dia,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin,
                        disponible=True
                    )

        # sabado (dia 5)
        if request.POST.get('libre_5') != 'on':
            hora_inicio_str = request.POST.get('hora_inicio_5')
            hora_fin_str = request.POST.get('hora_fin_5')
            if hora_inicio_str and hora_fin_str:
                hora_inicio = time.fromisoformat(hora_inicio_str)
                hora_fin = time.fromisoformat(hora_fin_str)
                if hora_inicio < hora_fin:
                    DisponibilidadMecanico.objects.create(
                        mecanico=mecanico,
                        dia_semana=5,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin,
                        disponible=True
                    )

        messages.success(request, 'Servicios y disponibilidad asignados correctamente.')
        return redirect('listar_mecanico')

    especialidad = mecanico.especialidad.lower().strip()
    servicios_disponibles = SERVICIOS_POR_ESPECIALIDAD.get(especialidad, [])
    


    return render(request, 'mecanico/asignar_servicios_disponibilidad.html', {
        'mecanico': mecanico,
        'servicios_disponibles': servicios_disponibles,
        'dias': DIA_SEMANA_CHOICES,
        'horas': [f'{h:02d}:00' for h in range(8, 21)],
        'duraciones': duraciones,
        'active': 'mecanicos'
    })