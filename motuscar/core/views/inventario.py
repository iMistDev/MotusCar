from django.shortcuts import render, redirect, get_object_or_404
from core.models.inventario import Products
from core.forms.inventario import ProductForm

# Create your views here.

def listar_productos(request):
    productos = Products.objects.all()
    return render(request, "inventario/listar.html", {"productos": productos})

def crear_productos(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductForm()
    return render(request, 'inventario/form.html', {'form': form})

def editar_producto(request, id):
    producto = get_object_or_404(Products, pk=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductForm(instance=producto)
        
    return render(request, 'inventario/form.html', {'form': form})

def eliminar_producto(request, id):
    producto = get_object_or_404(Products, pk=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'inventario/eliminar.html', {'producto': producto})
 