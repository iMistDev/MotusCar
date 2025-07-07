# dashboard/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from django.contrib import messages   # ← te faltaba este import

# ---- helpers ---------------------------------------------------------------

def admin_required(view_func):
    """
    Permite solo a usuarios autenticados con is_staff o superuser.
    """
    test = lambda u: u.is_authenticated and (u.is_staff or u.is_superuser)
    return user_passes_test(test)(view_func)

# ---- vistas ----------------------------------------------------------------

@admin_required                     # ← protege el panel
def dashboard_view(request):
    """
    Panel principal para administradores.
    """
    return render(request, "dashboard/dashboard.html")

def admin_login_view(request):
    """
    Formulario de login exclusivo para administradores.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and (user.is_staff or user.is_superuser):
            login(request, user)
            # Redirige al panel para evitar re‑envío del formulario
            return redirect(reverse("dashboard:admin_home"))
        else:
            messages.error(request, "Credenciales inválidas o no eres administrador.")

    # GET o POST fallido: muestra de nuevo el formulario
    return render(request, "dashboard/admin_login.html")
