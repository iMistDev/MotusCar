from django import forms
from core.models.vehiculo import Vehiculo
        
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'
        
        widgets = {
            'año': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['patente'].disabled = True
            self.fields['usuario'].disabled = True