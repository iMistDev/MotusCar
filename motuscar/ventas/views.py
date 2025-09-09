import math
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Max, Min
from core.models.inventario import Inventario
from core.models.productos import Products
from .models import Carrito, ItemCarrito, Orden
from core.constants.regiones import REGIONES_CHILE, COMUNAS_POR_REGION
from core.constants.repuestos import CATEGORIAS
import json
from django.db.models import Sum
from urllib.parse import urlencode
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
import json
from django.db import models
from reseñas.models import Reseña


def lista_productos(request):
    productos = Products.objects.all()

    # --- Filtros ---
    categoria = request.GET.get("categoria")
    region = request.GET.get("region")
    comuna = request.GET.get("comuna")
    orden = request.GET.get("orden")
    search = request.GET.get("search")
    # Calcular rango de precios real
    precio_maximo = productos.aggregate(Max('Precio_Unitario'))['Precio_Unitario__max'] or 150000
    precio_minimo = productos.aggregate(Min('Precio_Unitario'))['Precio_Unitario__min'] or 0

    # Asegurar que el mínimo sea 0 si hay productos gratuitos
    precio_minimo = max(0, precio_minimo)
    
    # Redondear a múltiplos de 1000 para mejor visualización
    precio_maximo = math.ceil(precio_maximo / 1000) * 1000
    precio_minimo = math.floor(precio_minimo / 1000) * 1000
    
    if categoria:
        productos = productos.filter(Categoria__icontains=categoria)

    # Filtrar por region/comuna a través de inventario → sucursal
    if region:
        productos = productos.filter(inventario__sucursal__region__iexact=region)
    if comuna:
        productos = productos.filter(inventario__sucursal__comuna__iexact=comuna)

    if search:
        productos = productos.filter(
            Q(Nombre_Producto__icontains=search) | Q(Descripcion__icontains=search)
        )
    

    # --- Ordenar ---
    if orden == "precio_asc":
        productos = productos.order_by("Precio_Unitario")
    elif orden == "precio_desc":
        productos = productos.order_by("-Precio_Unitario")

    productos = productos.distinct()

    # --- Comunas dinámicas ---
    TODAS_LAS_COMUNAS = sorted(
        list(set([c for comunas in COMUNAS_POR_REGION.values() for c in comunas]))
    )
    comunas = COMUNAS_POR_REGION.get(region, TODAS_LAS_COMUNAS) if region else TODAS_LAS_COMUNAS

    # --- Paginación ---
    paginator = Paginator(productos, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # --- Construir querystring para paginación ---
    qs = request.GET.copy()
    if "page" in qs:
        qs.pop("page")

    context = {
        "productos": page_obj,
        "page_obj": page_obj,
        "is_paginated": paginator.num_pages > 1,
        "categorias": CATEGORIAS,
        "regiones": REGIONES_CHILE,
        "comunas": comunas,
        "categoria_sel": categoria,
        "region_sel": region,
        "comuna_sel": comuna,
        "orden": orden,
        "search": search,
        "comunas_por_region_json": json.dumps(COMUNAS_POR_REGION),
        "querystring": urlencode(qs),
        'precio_maximo': precio_maximo,
        'precio_minimo': precio_minimo,
    }
    return render(request, "ventas/lista_productos.html", context)



def detalle_producto(request, producto_id):
    producto = get_object_or_404(Products, id_producto=producto_id)

    # Stock por sucursal del proveedor del producto
    stock_por_sucursal = Inventario.objects.filter(producto=producto).values('sucursal__nombre', 'sucursal__comuna').annotate(stock=Sum('cantidad'))
    reseñas = Reseña.objects.filter(producto=producto).order_by('-creado')

    # Total stock del producto del proveedor (para habilitar el botón)
    total_stock = stock_por_sucursal.aggregate(total=Sum('stock'))['total'] or 0

    # Otros proveedores que tienen el mismo producto
    otros_proveedores = Products.objects.filter(Nombre_Producto=producto.Nombre_Producto).exclude(id_producto=producto.id_producto)

    otros_stock = []
    for prod in otros_proveedores:
        stock = Inventario.objects.filter(producto=prod).values('sucursal__nombre', 'sucursal__comuna').annotate(stock=Sum('cantidad'))
        otros_stock.append({
            'proveedor': prod.Proveedor.nombre,
            'precio': prod.Precio_Unitario,
            'stock': stock
        })

    return render(request, 'ventas/detalle_producto.html', {
        'producto': producto,
        'stock_por_sucursal': stock_por_sucursal,
        'otros_stock': otros_stock,
        'total_stock': total_stock,
        'reseñas': reseñas
    })

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
        if not items.exists():
            messages.error(request, 'Tu carrito está vacío.')
            return redirect('lista_productos_repuestos')

        # Crear la orden
        orden = Orden.objects.create(total=total, usuario=request.user)

        # Tomamos el primer producto para la redirección (puedes cambiar la lógica si hay varios)
        primer_item = items.first()
        producto_id = primer_item.producto.id_producto

        # Vaciar el carrito
        items.delete()

        messages.success(request, '¡Compra realizada con éxito! Gracias por tu compra.')

        # Redirigir a la página de crear reseña
        return redirect('crear_reseña', producto_id=producto_id, orden_id=orden.id)

    # Si es GET, mostramos el checkout
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