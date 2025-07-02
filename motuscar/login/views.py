from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm

def login_view(request):
# Si el usuario ya está autenticado, redirigir al home
    if request.user.is_authenticated:
        return redirect('landing')

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
    # Si el usuario ya está autenticado, redirigir al home
    if request.user.is_authenticated:
        return redirect('landing')  # Cambia 'home' por 'landing' si prefieres

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email.split('@')[0]  # auto-username
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            messages.success(request, f'Cuenta creada para {user.email}! Ahora puedes iniciar sesión')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

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
