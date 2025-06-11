from django import forms
from core.models.mecanico import Mecanico

class MecanicoForm(forms.ModelForm):
    class Meta:
        model = Mecanico
        fields = '__all__'