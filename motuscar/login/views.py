import json
import time
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import time, timedelta
from django.urls import reverse   # ←  nuevo import

from core.constants.regiones import COMUNAS_POR_REGION
from core.constants.servicios import SERVICIOS_POR_ESPECIALIDAD
from core.forms.mecanico import  Mecanico2Form
from core.models.disponibilidad import DisponibilidadMecanico
from core.models.mecanico import Mecanico
from core.models.servicio import Servicio
from core.models.usuario_comun import UsuarioComun
from core.views.mecanico import DIA_SEMANA_CHOICES
from login.models import CustomUser
from .forms import LoginForm, RegisterForm
from core.models.vehiculo import Vehiculo
from core.forms.vehiculo import VehiculoForm
#
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_view(request):
# Si el usuario ya está autenticado, redirigir al home
    if request.user.is_authenticated:
        return redirect('motus')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        #permite controlar login para customuser y mecanico:
        if form.is_valid():
            email = form.cleaned_data.get('username')  #usa el email como USERNAME
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                nombre = ''
                if hasattr(user, 'first_name'):
                    nombre = f"{user.first_name} {user.last_name}".strip()
                elif hasattr(user, 'nombre'):
                    nombre = f"{user.nombre} {user.apellido}".strip()
                else:
                    nombre = user.email

                # luego de darle al boton de login #redirige aqui a la pagina de inicio:
                messages.success(request, f'Bienvenido {nombre}!')
                return redirect(request.GET.get('next', 'motus'))
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Por favor corrige los errores')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        tipo_usuario = request.POST.get('tipo')

        if form.is_valid() and tipo_usuario:
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Este correo ya está registrado.')
            else:
                if tipo_usuario == 'mecanico':
                    user = Mecanico(  # instancia Mecanico
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=email,
                        username=email,
                    )
                else:
                    user = UsuarioComun( # instancia Usuario
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=email,
                        username=email,
                    )

                user.set_password(form.cleaned_data['password1'])
                user.save()
                request.session['user_id_registro'] = user.id

                if tipo_usuario == 'mecanico':
                    return redirect('datos_mecanico')
                elif tipo_usuario == 'usuario':
                    messages.success(request, 'Usuario registrado correctamente.')
                    return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def datos_mecanico(request):
    user_id = request.session.get('user_id_registro')
    if not user_id:
        return redirect('register')

    # ya es instancia de Mecanico (porque lo fue al registrarse)
    mecanico = get_object_or_404(Mecanico, id=user_id)

    if request.method == 'POST':
        form = Mecanico2Form(request.POST, instance=mecanico)
        if form.is_valid():
            form.save()
            del request.session['user_id_registro']
            return redirect('asignar_servicios', mecanico_id=mecanico.id)
    else:
        form = Mecanico2Form(instance=mecanico)

    return render(request, 'datos_mecanico.html', {
        'form': form,
        'comunas_por_region_json': json.dumps(COMUNAS_POR_REGION),
        'active': 'mecanicos'
    })


def asignar_servicios(request, mecanico_id):
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

        messages.success(request, 'Usuario registrado correctamente.')
        messages.success(request, 'Servicios y disponibilidad asignados correctamente.')
        return redirect('login')

    especialidad = mecanico.especialidad.lower().strip()
    servicios_disponibles = SERVICIOS_POR_ESPECIALIDAD.get(especialidad, [])
    


    return render(request, 'asignar_servicios.html', {
        'mecanico': mecanico,
        'servicios_disponibles': servicios_disponibles,
        'dias': DIA_SEMANA_CHOICES,
        'horas': [f'{h:02d}:00' for h in range(8, 21)],
        'duraciones': duraciones,
        'active': 'mecanicos'
    })


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('login')


@login_required
def perf_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def landing_view(request):
    return render(request, 'landing.html', {'user': request.user})





@login_required
def vista_vehiculos_usuario(request):
    usuario_comun = UsuarioComun.objects.get(id=request.user.id)
    vehiculos = Vehiculo.objects.filter(usuario=usuario_comun, deleted__isnull=True)
    return render(request, 'vehiculo/listar.html',  {'vehiculos': vehiculos})

@login_required
def crear_vehiculo(request):
    usuario_comun = UsuarioComun.objects.get(id=request.user.id)
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.usuario = usuario_comun
            vehiculo.save()
            return redirect('mis_vehiculos')
    else:
        form = VehiculoForm()
    return render(request, 'vehiculo/crear.html', {'form': form})


@login_required
def editar_vehiculo(request, vehiculo_id):
    usuario_comun = UsuarioComun.objects.get(id=request.user.id)

    vehiculo = Vehiculo.objects.filter(id=vehiculo_id).first()

    vehiculo = Vehiculo.objects.filter(id=vehiculo_id, usuario=usuario_comun, deleted__isnull=True).first()

    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('mis_vehiculos')
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(request, 'vehiculo/editar.html', {'form': form})

@login_required
def eliminar_vehiculo(request, vehiculo_id):
    usuario_comun = UsuarioComun.objects.get(id=request.user.id)
    
    # Obtener vehículo solo si pertenece al usuario y no está eliminado
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id, usuario=usuario_comun, deleted__isnull=True)
    
    if request.method == 'POST':
        vehiculo.delete()  # Soft delete por SafeDelete
        messages.success(request, f'Vehículo {vehiculo.patente} eliminado correctamente.')
        return redirect('mis_vehiculos')

    # Si quieres, muestra una confirmación antes de eliminar
    return render(request, 'vehiculo/eliminar_definitivo.html', {'vehiculo': vehiculo})



#vista de administrador (login_required)
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                # ‼️ Redirección al dashboard de administradores:
                return render(request, 'dashboard/dashboard.html', {'user': user})
            else:
                messages.error(request, "No tienes permisos de administrador.")
        else:
            messages.error(request, "Credenciales inválidas.")
    return render(request, 'login/admin_login.html')