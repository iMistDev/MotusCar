from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import CustomUser  # Import directly from models

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )
    
    error_messages = {
        'invalid_login': _(
            "Por favor ingresa un email y contraseña correctos. "
            "Nota que ambos campos pueden ser sensibles a mayúsculas."
        ),
        'inactive': _("Esta cuenta está inactiva."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'autocomplete': 'email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'autocomplete': 'current-password'
        })


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'ejemplo@dominio.com',
            'autocomplete': 'email'
        }),
        max_length=254,
        help_text=_("Requerido. Ingresa una dirección de correo válida.")
    )
    
    first_name = forms.CharField(
        label=_("Nombre"),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Tu nombre',
            'autocomplete': 'given-name'
        })
    )

    last_name = forms.CharField(
        label=_("Apellido"),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Tu apellido',
            'autocomplete': 'family-name'
        })
    )
    
    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Contraseña',
            'autocomplete': 'new-password'
        }),
        help_text=_(
            "Tu contraseña debe contener al menos 8 caracteres, "
            "no puede ser completamente numérica y no puede ser similar a tu nombre de usuario."
        )
    )
    
    password2 = forms.CharField(
        label=_("Confirmación de contraseña"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Repite tu contraseña',
            'autocomplete': 'new-password'
        }),
        help_text=_("Ingresa la misma contraseña que antes, para verificación.")
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name','email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                _("Este correo electrónico ya está registrado."),
                code='email_exists'
            )
        return email
    

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mejora los mensajes de error
        self.fields['password1'].error_messages = {
            'password_too_short': _("La contraseña es demasiado corta."),
            'password_common': _("La contraseña es demasiado común."),
            'password_entirely_numeric': _("La contraseña no puede ser completamente numérica."),
        }


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label=_("Correo electrónico"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ingresa tu correo electrónico',
            'autocomplete': 'email'
        })
    )


class PasswordResetForm(forms.Form):
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nueva contraseña',
            'autocomplete': 'new-password'
        }),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirmar nueva contraseña',
            'autocomplete': 'new-password'
        }),
        strip=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                _("Las contraseñas no coinciden."),
                code='password_mismatch'
            )
        
        return cleaned_data
    

#formulario perfil
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
                
                
                
                
# PARA CREAR SUBCLASES - NO BORRAR !!!
class SubClasesForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@dominio.com'}),
        max_length=254
    )

    first_name = forms.CharField(
        label=_("Nombre"),
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tu nombre'})
    )

    last_name = forms.CharField(
        label=_("Apellido"),
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tu apellido'})
    )

    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Contraseña'})
    )

    password2 = forms.CharField(
        label=_("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Repite tu contraseña'})
    )

    class Meta:
        model = CustomUser  # la diferencia importante !
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Este correo electrónico ya está registrado."))
        return email
    
    
# PARA EDITAR, EL OTRO CREA NO BORRAR !!!
class EditarUsuarioForm(forms.ModelForm):
    email = forms.EmailField(
        label=("Correo electrónico"),
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Correo electrónico'
        })
    )
    first_name = forms.CharField(
        label=("Nombre"),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nombre'
        })
    )
    last_name = forms.CharField(
        label=("Apellido"),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Apellido'
        })
    )
 
    password1 = forms.CharField(
        label=("Nueva contraseña"),
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nueva contraseña'
        })
    )

    password2 = forms.CharField(
        label=("Confirmar nueva contraseña"),
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Repite nueva contraseña'
        })
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(_("Este correo electrónico ya está en uso."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError(_("Las contraseñas no coinciden."))
            if len(password1) < 8:
                raise forms.ValidationError(_("La contraseña debe tener al menos 8 caracteres."))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
    