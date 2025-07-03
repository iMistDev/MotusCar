from django import forms
from core.models.usuario_comun import UsuarioComun

class UsuarioComunForm(forms.ModelForm):
    class Meta:
        model = UsuarioComun
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UsuarioComun.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email
    
    def save(self, commit=True):
        usuario_comun = super().save(commit=False)
        # contraseña cifrada
        password = self.cleaned_data.get('password')
        if password:
            usuario_comun.set_password(password)
        if commit:
            usuario_comun.save()
            self.save_m2m()
        return usuario_comun

class UsuarioComunEditarForm(forms.ModelForm):
    nueva_contraseña = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = UsuarioComun
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        usuario = super().save(commit=False)
        nueva_password = self.cleaned_data.get('nueva_contraseña')
        if nueva_password:
            usuario.set_password(nueva_password)
        if commit:
            usuario.save()
        return usuario