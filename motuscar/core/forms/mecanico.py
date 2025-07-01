from django import forms
from core.models.mecanico import Mecanico

from core.constants.regiones import REGIONES_CHILE, COMUNAS_POR_REGION
from core.constants.servicios import ESPECIALIDAD, TIPOS

class MecanicoForm(forms.ModelForm):
    class Meta:
        model = Mecanico
        fields = ['nombre', 'apellido', 'email', 'region', 'comuna', 'direccion', 'especialidad', 'tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'region': forms.Select(choices=REGIONES_CHILE, attrs={'class': 'form-select', 'id': 'region'}),
            'comuna': forms.Select(attrs={'class': 'form-select', 'id': 'comuna'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(choices=ESPECIALIDAD, attrs={'class': 'form-select'}),
            'tipo': forms.Select(choices=TIPOS, attrs={'class': 'form-select'}),
        }
        
        error_messages = {
            'nombre': {
                'required': 'Por favor, ingresa el nombre del mecánico.',
                'max_length': 'El nombre no puede exceder los 50 caracteres.',
            },
            'apellido': {
                'required': 'Por favor, ingresa el apellido del mecánico.',
                'max_length': 'El apellido no puede exceder los 50 caracteres.',
            },
            'email': {
                'required': 'Por favor, ingresa un correo electrónico.',
                'invalid': 'El correo ingresado no es válido.',
                'unique': 'Este correo ya está registrado.',
            },
            'region': {
                'required': 'Selecciona una región.',
            },
            'comuna': {
                'required': 'Selecciona una comuna.',
            },
            'direccion': {
                'required': 'Ingresa la dirección del mecánico.',
                'max_length': 'La dirección es demasiado larga.',
            },
            'especialidad': {
                'required': 'Selecciona una especialidad.',
            },
            'tipo': {
                'required': 'Selecciona el tipo de mecánico.',
            },
        }