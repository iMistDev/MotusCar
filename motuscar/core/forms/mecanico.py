from django import forms
from core.models.mecanico import Mecanico

from core.constants.regiones import REGIONES_CHILE, COMUNAS_POR_REGION
from core.constants.servicios import ESPECIALIDAD, TIPOS
    
class MecanicoForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Mecanico
        fields = ['first_name', 'last_name', 'email', 'username', 'region', 'comuna', 'direccion', 'especialidad', 'tipo', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'region': forms.Select(choices=REGIONES_CHILE, attrs={'class': 'form-select', 'id': 'region'}),
            'comuna': forms.Select(attrs={'class': 'form-select', 'id': 'comuna'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(choices=ESPECIALIDAD, attrs={'class': 'form-select'}),
            'tipo': forms.Select(choices=TIPOS, attrs={'class': 'form-select'}),
        }
        
        error_messages = {
            'first_name': {
                'required': 'Por favor, ingresa el nombre del mecánico.',
                'max_length': 'El nombre no puede exceder los 150 caracteres.',
            },
            'last_name': {
                'required': 'Por favor, ingresa el apellido del mecánico.',
                'max_length': 'El apellido no puede exceder los 150 caracteres.',
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
        
    def save(self, commit=True):
        mecanico = super().save(commit=False)
        mecanico.set_password(self.cleaned_data['password'])
        if commit:
            mecanico.save()
        return mecanico