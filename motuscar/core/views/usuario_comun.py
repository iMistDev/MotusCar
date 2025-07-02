from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models.usuario_comun import UsuarioComun
from core.forms.usuario_comun import UsuarioComunForm
from django.views.generic import DeleteView
from django.urls import reverse_lazy


def listar_usuario_comun(request):
    usuarios = UsuarioComun.objects.all()
    return render(request, 'usuario_comun/user_list.html', {'usuarios': usuarios})


def crear_usuario_comun(request):
    if request.method == 'POST':
        form = UsuarioComunForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario común creado correctamente.")
            return redirect('listar_usuario_comun')
    else:
        form = UsuarioComunForm()
    return render(request, 'usuario_comun/user_forms.html', {'form': form, 'titulo': 'Crear Usuario Común'})

def editar_usuario_comun(request, pk):
    usuario = get_object_or_404(UsuarioComun, pk=pk)
    form = UsuarioComunForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        messages.success(request, "Usuario común actualizado.")
        return redirect('listar_usuario_comun')
    return render(request, 'usuario_comun/user_forms.html', {'form': form, 'titulo': 'Editar Usuario Común'})

class EliminarUsuarioComun(DeleteView):
    model = UsuarioComun
    template_name = 'usuario_comun/user_confirm_delete.html'
    success_url = reverse_lazy('listar_usuario_comun')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Usuario común eliminado.")
        return super().delete(request, *args, **kwargs)
