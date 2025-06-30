from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm


def login_view(request):
    # Si el usuario ya está autenticado, redirigir al home
    if request.user.is_authenticated:
        return redirect('landing')  # Opcional: puedes cambiarlo a 'landing' si prefieres

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}!')
                # Luego de darle al boton de login #redirige aqui a la pagina de inicio
                next_url = request.GET.get('next', 'motus')  # Redirige a 'motus (home page)' por defecto
                return redirect(next_url)
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
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}! Ahora puedes iniciar sesión')
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
