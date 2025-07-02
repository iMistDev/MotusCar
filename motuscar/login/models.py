from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Teléfono'))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_('Fecha de nacimiento'))
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_('Foto de perfil'))

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return self.email

class PerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+56 9 1234 5678'
            }),
        }
        labels = {
            'first_name': _('Nombres'),
            'last_name': _('Apellidos'),
            'phone': _('Teléfono'),
            'birth_date': _('Fecha de nacimiento'),
            'avatar': _('Foto de perfil')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-input'})