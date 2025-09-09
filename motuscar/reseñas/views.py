from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Reseña
from ventas.models import Orden
from core.models.productos import Products
from login.models import CustomUser

def crear_reseña(request, producto_id, orden_id):
    # Asegurarse de que el usuario esté logeado
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para dejar una reseña.")
        return redirect('login')

    # Obtener la orden y verificar que pertenezca al usuario
    orden = get_object_or_404(Orden, id=orden_id, usuario=request.user)




    # Obtener el producto
    producto = get_object_or_404(Products, id_producto=producto_id)


    # Verificar si ya existe una reseña para esta orden y producto
    if Reseña.objects.filter(producto=producto, usuario=request.user, orden=orden).exists():
        messages.error(request, "Ya has dejado una reseña para este producto en esta orden.")
        return redirect('detalle_producto', producto_id=producto_id)

    if request.method == 'POST':
        calificacion = int(request.POST.get('calificacion', 5))
        comentario = request.POST.get('comentario', '').strip()

        Reseña.objects.create(
            producto=producto,
            usuario=request.user,
            orden=orden,
            calificacion=calificacion,
            comentario=comentario
        )
        messages.success(request, "¡Reseña creada exitosamente!")
        return redirect('detalle_producto', producto_id=producto_id)

    return render(request, 'crear_reseña.html', {
        'producto': producto,
        'orden': orden
    })
