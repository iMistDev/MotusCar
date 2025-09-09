from django import forms
from core.models.productos import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'