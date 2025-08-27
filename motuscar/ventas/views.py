from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models.inventario import Products
from .models import Carrito, ItemCarrito, Orden

def lista_productos(request):
    productos_list = Products.objects.all()
    paginator = Paginator(productos_list, 9)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener información del carrito para el contador
    carrito = _get_or_create_carrito(request)
    items_carrito = ItemCarrito.objects.filter(carrito=carrito)
    
    return render(request, 'ventas/lista_productos.html', {
        'productos': page_obj,
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'items': items_carrito
    })

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Products, id_producto=producto_id)
    return render(request, 'ventas/detalle_producto.html', {'producto': producto})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Products, id_producto=producto_id)
    carrito = _get_or_create_carrito(request)
    
    item = ItemCarrito.objects.filter(carrito=carrito, producto=producto).first()
    
    if item:
        item.cantidad += 1
        item.save()
        messages.success(request, f'✅ Se agregó otra unidad de "{producto.Nombre_Producto}" al carrito')
    else:
        ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=1)
        messages.success(request, f'🎉 ¡"{producto.Nombre_Producto}" agregado al carrito con éxito!')
    
    return redirect('lista_productos_repuestos')
def ver_carrito(request):
    carrito = _get_or_create_carrito(request)
    items = ItemCarrito.objects.filter(carrito=carrito)
    total = sum(item.subtotal() for item in items)
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(ItemCarrito, id=item_id, carrito=carrito)
        
        if 'actualizar' in request.POST:
            nueva_cantidad = request.POST.get('cantidad')
            if nueva_cantidad and nueva_cantidad.isdigit():
                item.cantidad = int(nueva_cantidad)
                item.save()
                messages.success(request, f'📊 Cantidad de {item.producto.Nombre_Producto} actualizada')
        
        elif 'eliminar' in request.POST:
            nombre_producto = item.producto.Nombre_Producto
            item.delete()
            messages.success(request, f'🗑️ {nombre_producto} eliminado del carrito')
        
        return redirect('ver_carrito')
    
    return render(request, 'ventas/ver_carrito.html', {'items': items, 'total': total})

def checkout(request):
    carrito = _get_or_create_carrito(request)
    items = ItemCarrito.objects.filter(carrito=carrito)
    total = sum(item.subtotal() for item in items)
    
    if request.method == 'POST':
        Orden.objects.create(total=total)
        items.delete()
        messages.success(request, '¡Compra realizada con éxito! Gracias por tu compra.')
        return redirect('lista_productos_repuestos')
    
    return render(request, 'ventas/checkout.html', {'items': items, 'total': total})

def _get_or_create_carrito(request):
    carrito_id = request.session.get('carrito_id')
    if carrito_id:
        try:
            carrito = Carrito.objects.get(id=carrito_id)
        except Carrito.DoesNotExist:
            carrito = Carrito.objects.create()
            request.session['carrito_id'] = carrito.id
    else:
        carrito = Carrito.objects.create()
        request.session['carrito_id'] = carrito.id
    return carrito