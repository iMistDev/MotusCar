from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models.mecanico import Mecanico
from core.forms.mecanico import MecanicoForm

#ESTAS VIEWS NO TIENEN TEMPLATES, SON SOLO PARA INGRESAR DATOS DE PRUEBA

def home(request):
    return render(request, 'index.html')

def listar_mecanico(request):
    mecanicos = Mecanico.objects.all()
    return render(request, 'mecanico/listar.html', {'mecanicos': mecanicos, 'active': 'listar'})

 
def crear_mecanico(request):
    if request.method == 'POST':
        form = MecanicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Creado')
            return redirect('listar_mecanico')
    else:
        form = MecanicoForm()
    return render(request, 'mecanico/crear.html', {'form': form, 'active': 'crear'})