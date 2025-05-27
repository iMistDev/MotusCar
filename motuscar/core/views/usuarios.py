from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from core.forms.usuarios import UserForm
from django.views.generic import DeleteView
from django.urls import reverse_lazy

def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'usuarios/user_list.html', {'users': users})

def user_manage(request, pk=None):
    user = get_object_or_404(User, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        
        if form.is_valid():
            user = form.save()
            action = "actualizado" if pk else "creado"
            messages.success(request, f'Usuario {user.username} {action} correctamente!')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    
    context = {
        'form': form,
        'title': 'Editar Usuario' if pk else 'Crear Usuario'
    }
    return render(request, 'usuarios/user_form.html', context)

class UserDeleteView(DeleteView):
    model = User
    template_name = 'usuarios/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Usuario eliminado correctamente!')
        return super().delete(request, *args, **kwargs)