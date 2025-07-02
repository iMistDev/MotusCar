# Modelos
from core.models.mecanico import Mecanico
from core.models.servicio import Servicio
from core.models.agenda import Agenda
from core.models.disponibilidad import DisponibilidadMecanico


# Importacion de archivos
from core.forms.agenda import AgendaForm
from core.constants.regiones import REGIONES_CHILE, COMUNAS_POR_REGION

# Librerias
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import date, datetime, timedelta, time
from django.db.models import Q
from django.core.exceptions import ValidationError


# homepage
def home(request):
    return render(request, 'index.html')

# listar mecanicos con filtros
@login_required
def listar_mecanicos(request):
    # obtener todos los mecanicos
    mecanicos = Mecanico.objects.all()
    region = request.GET.get('region')
   # print("REGION:", repr(region))

    comuna = request.GET.get('comuna')
    especialidad = request.GET.get('especialidad')
    servicio_id = request.GET.get('servicio')
    
    # aplicar filtros
    if region:
        region_lower = region.strip().lower()
        mecanicos = mecanicos.filter(region__iexact=region_lower)
        #print("Filtrando región con:", repr(region_db))
        #print("Mecánicos encontrados:", mecanicos)


    if comuna:
        # filtro sin contar mayusculas - minusculas
        mecanicos = mecanicos.filter(comuna__iexact=comuna)

    if especialidad:
        # normalizar nombres de especialidad
        especialidad_lower = especialidad.lower()
        especialidad_map = {
            'electrico': 'electrico',
            'eléctrico': 'electrico',
            'vulcanizacion': 'vulcanizacion',
            'vulcanización': 'vulcanizacion',
            'mecanica': 'mecanica',
            'mecánica': 'mecanica',
        }
        especialidad_db = especialidad_map.get(especialidad_lower, especialidad_lower)
        mecanicos = mecanicos.filter(especialidad__iexact=especialidad_db)

    if servicio_id:
        # filtrar por id de servicio
        mecanicos = mecanicos.filter(servicio__id=servicio_id)

    # eliminar duplicados
    mecanicos = mecanicos.distinct()

    # preparar lista de comunas para el template
    TODAS_LAS_COMUNAS = []
    for comunas_region in COMUNAS_POR_REGION.values():
        TODAS_LAS_COMUNAS.extend(comunas_region)
    TODAS_LAS_COMUNAS = sorted(list(set(TODAS_LAS_COMUNAS)))

    # filtrar comunas por region si se especifico una
    comunas = COMUNAS_POR_REGION.get(region, TODAS_LAS_COMUNAS) if region else TODAS_LAS_COMUNAS

    # preparar diccionario de servicios por especialidad
    servicios_por_especialidad = {}
    for mecanico in Mecanico.objects.all():
        esp = mecanico.especialidad.lower()
        if esp not in servicios_por_especialidad:
            servicios_por_especialidad[esp] = []

        for servicio in mecanico.servicio_set.all():
            if servicio.id not in [s['id'] for s in servicios_por_especialidad[esp]]:
                servicios_por_especialidad[esp].append({
                    'id': servicio.id,
                    'nombre': servicio.nombre
                })
                
    # construir contexto para el template
    context = {
        'mecanicos': mecanicos,
        'regiones': REGIONES_CHILE, 
        'comunas': comunas,
        'especialidades': Mecanico.objects.values_list('especialidad', flat=True).distinct(),
        'servicios': Servicio.objects.all(),
        'region_sel': region,
        'comuna_sel': comuna,
        'especialidad_sel': especialidad,
        'servicio_sel': servicio_id,
       # 'mecanico': mecanico,
        'active': 'agendar',
        'comunas_por_region_json': json.dumps(COMUNAS_POR_REGION),
        'servicios_por_especialidad_json': json.dumps(servicios_por_especialidad),
    }
    
    return render(request, 'agenda/listar_mecanicos.html', context)

# vista para agendar una cita
@login_required
def agendar_cita(request, mecanico_id, servicio_id):
    # obtener mecanico y servicio o devolver 404 si no existen
    mecanico = get_object_or_404(Mecanico, pk=mecanico_id)
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    
    if request.method == 'POST':
        # procesar formulario de agendar
        fecha_str = request.POST.get('fecha')
        hora_inicio_str = request.POST.get('hora_inicio')
        
        try:
            # convertir y validar formatos de fecha - hora
            fecha = datetime.strptime(fecha_str, '%d/%m/%Y').date()
          #  fecha_api_format = fecha.strftime('%Y-%m-%d')
            hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
            hora_fin = (datetime.combine(date.today(), hora_inicio) + servicio.duracion_estimada).time()
            
            # validar disponibilidad del horario
            citas_existentes = Agenda.objects.filter(
                mecanico=mecanico,
                fecha=fecha,
                hora_inicio=hora_inicio
            ).exists()
            
            if citas_existentes:
                messages.error(request, 'Ya existe una cita agendada en ese horario')
                return redirect('agendar_cita', mecanico_id=mecanico_id, servicio_id=servicio_id)
            
            # verificar solapamiento con otras citas
            citas_solapadas = Agenda.objects.filter(
                mecanico=mecanico,
                fecha=fecha,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            ).exists()
            
            if citas_solapadas:
                messages.error(request, 'El horario seleccionado se solapa con otra cita existente')
                return redirect('agendar_cita', mecanico_id=mecanico_id, servicio_id=servicio_id)
            
            # verificar disponibilidad del mecanico
            dia_semana = fecha.weekday()
            disponibilidad = DisponibilidadMecanico.objects.filter(
                mecanico=mecanico,
                dia_semana=dia_semana,
                disponible=True,
                hora_inicio__lte=hora_inicio,
                hora_fin__gte=hora_inicio
            ).exists()
            
            if not disponibilidad:
                messages.error(request, 'El mecánico no está disponible en ese horario')
                return redirect('agendar_cita', mecanico_id=mecanico_id, servicio_id=servicio_id)
            
            # verificar que la duracion del servicio no exceda el horario disponible
            #ej: no se permite un servicio de 5 horas cuando quedan 2 horas de jornada
            horario_dia = DisponibilidadMecanico.objects.get(
                mecanico=mecanico,
                dia_semana=dia_semana
            )
            if hora_fin > horario_dia.hora_fin:
                messages.error(request, 'El servicio no cabe en el horario disponible')
                return redirect('agendar_cita', mecanico_id=mecanico_id, servicio_id=servicio_id)
            
            # crear la cita si pasa todas las validaciones
            Agenda.objects.create(
                mecanico=mecanico,
                servicio=servicio,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                estado='pendiente',
                descripcion=f'Cita agendada para {servicio.nombre}'
            )
            messages.success(request, 'Cita agendada exitosamente')
            return redirect('listar_agenda')
            
        except ValueError:
            messages.error(request, 'Formato de fecha u hora inválido')
            return redirect('agendar_cita', mecanico_id=mecanico_id, servicio_id=servicio_id)
    
    # obtener disponibilidad para mostrar en el template
    disponibilidad = DisponibilidadMecanico.objects.filter(
        mecanico=mecanico,
        disponible=True
    ).order_by('dia_semana', 'hora_inicio')

    return render(request, 'agenda/agendar_cita.html', {
        'mecanico': mecanico,
        'active': 'agendar',
        'servicio': servicio,
        'disponibilidad': disponibilidad,
        'dias_semana': dict(DisponibilidadMecanico._meta.get_field('dia_semana').choices)
    })

# vista para listar citas agendadas
@login_required
def listar_agenda(request):
    hoy = date.today()
    ahora = timezone.now().time()
    
    # obtener todas las citas (debería filtrar por usuario)
    todas_citas = Agenda.objects.all()
    
    # clasificar citas en tres categorias para el orden en listar
    citas_hoy = []
    citas_futuras = []
    citas_pasadas = []
    
    for agenda in todas_citas:
        if agenda.fecha == hoy:
            if agenda.hora_inicio > ahora:
                citas_hoy.append(agenda)  # citas de hoy pendientes
            else:
                citas_pasadas.append(agenda)  # citas de hoy ya pasadas
        elif agenda.fecha > hoy:
            citas_futuras.append(agenda)
        else:
            citas_pasadas.append(agenda)
    
    # ordenar cada categoria
    citas_hoy.sort(key=lambda x: x.hora_inicio)
    citas_futuras.sort(key=lambda x: (x.fecha, x.hora_inicio))
    citas_pasadas.sort(key=lambda x: (-x.fecha.year, -x.fecha.month, -x.fecha.day, x.hora_inicio))
    
    # combinar todas las citas ordenadas
    agendas_ordenadas = citas_hoy + citas_futuras + citas_pasadas
    
    return render(request, 'agenda/listar.html', {
        'agendas': agendas_ordenadas,
        'active': 'agenda'
    })

# vista para editar una cita existente
@login_required
def editar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, pk=agenda_id)
    
    if request.method == 'POST':
        nueva_hora_str = request.POST.get('hora_inicio')
        
        try:
            # validar y procesar nueva hora
            nueva_hora = datetime.strptime(nueva_hora_str, '%H:%M').time()
            
            if nueva_hora == agenda.hora_inicio:
                messages.info(request, 'No se realizaron cambios en la hora de la cita')
                return redirect('listar_agenda')
            
            # calcular nueva hora de fin
            duracion = agenda.servicio.duracion_estimada
            nueva_hora_fin = (datetime.combine(date.today(), nueva_hora) + duracion).time()
            
            # validar disponibilidad del mecanico
            dia_semana = agenda.fecha.weekday()
            disponibilidad = DisponibilidadMecanico.objects.filter(
                mecanico=agenda.mecanico,
                dia_semana=dia_semana,
                disponible=True
            ).first()
            
            if not disponibilidad:
                messages.error(request, 'El mecánico no trabaja este día')
                return redirect('editar_agenda', agenda_id=agenda.id)
            
            # validar horario dentro de disponibilidad
            if nueva_hora < disponibilidad.hora_inicio or nueva_hora_fin > disponibilidad.hora_fin:
                messages.error(request, 'El horario seleccionado está fuera del horario de trabajo del mecánico')
                return redirect('editar_agenda', agenda_id=agenda.id)
            
            # verificar solapamiento con otras citas
            citas_solapadas = Agenda.objects.filter(
                mecanico=agenda.mecanico,
                fecha=agenda.fecha,
                hora_inicio__lt=nueva_hora_fin,
                hora_fin__gt=nueva_hora
            ).exclude(id=agenda.id).exists()
            
            if citas_solapadas:
                messages.error(request, 'El nuevo horario se solapa con otra cita existente')
                return redirect('editar_agenda', agenda_id=agenda.id)
            
            # actualizar cita si pasa validaciones
            agenda.hora_inicio = nueva_hora
            agenda.hora_fin = nueva_hora_fin
            agenda.save()
            
            messages.success(request, 'Cita actualizada correctamente')
            return redirect('listar_agenda')
            
        except ValueError:
            messages.error(request, 'Formato de hora inválido')
            return redirect('editar_agenda', agenda_id=agenda.id)
    
    return render(request, 'agenda/editar.html', {
        'agenda': agenda,
        'servicio': agenda.servicio,
        'active':'agenda'
    })

# vista para eliminar una cita
@login_required
def eliminar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda.objects.all(), pk=agenda_id)
    if request.method == 'POST':
        agenda.delete()
        messages.success(request, f'Cita eliminada')
        return redirect('listar_agenda')
    return render(request, 'agenda/eliminar.html', {'agenda': agenda, 'active': 'agenda'})

# vista API que devuelve horarios ocupados en formato JSON
def horarios_ocupados(request):
    mecanico_id = request.GET.get('mecanico_id')
    fecha_str = request.GET.get('fecha')
    
    try:
        # validar parametros
        mecanico_id = int(mecanico_id)
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return JsonResponse([], safe=False)
    
    # obtener citas no canceladas
    citas = Agenda.objects.filter(
        mecanico_id=mecanico_id,
        fecha=fecha
    ).exclude(estado='cancelada')
    
    # preparar respuesta JSON
    horarios = []
    for cita in citas:
        horarios.append({
            'inicio': datetime.combine(cita.fecha, cita.hora_inicio).isoformat(),
            'fin': datetime.combine(cita.fecha, cita.hora_fin).isoformat()
        })
    
    return JsonResponse(horarios, safe=False)