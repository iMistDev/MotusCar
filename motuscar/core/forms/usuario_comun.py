from django import forms
from core.models.usuario_comun import UsuarioComun
from django.contrib.auth.forms import UserCreationForm

class UsuarioComunForm(UserCreationForm):
    class Meta:
        model = UsuarioComun
        fields = ['first_name', 'last_name', 'email', 'telefono', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UsuarioComun.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email