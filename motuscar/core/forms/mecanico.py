from django import forms
from core.models.mecanico import Mecanico

from core.constants.regiones import REGIONES_CHILE, COMUNAS_POR_REGION
from core.constants.servicios import ESPECIALIDAD, TIPOS
    
class MecanicoForm(forms.ModelForm):
    class Meta:
        model = Mecanico
        fields = ['region', 'comuna', 'direccion', 'especialidad', 'tipo']
        widgets = {
            'region': forms.Select(choices=REGIONES_CHILE, attrs={'class': 'form-select', 'id': 'region'}),
            'comuna': forms.Select(attrs={'class': 'form-select', 'id': 'comuna'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(choices=ESPECIALIDAD, attrs={'class': 'form-select'}),
            'tipo': forms.Select(choices=TIPOS, attrs={'class': 'form-select'}),
        }
        
        error_messages = {
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
        if commit:
            mecanico.save()
        return mecanico
    
