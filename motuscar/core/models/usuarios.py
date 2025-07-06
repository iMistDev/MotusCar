# usuarios/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class UsuarioManager(BaseUserManager):
    """Manager personalizado para el modelo Usuario"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario con el email y contraseña dados"""
        if not email:
            raise ValueError(_('El Email debe ser proporcionado'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un superusuario"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuario debe tener is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuario debe tener is_superuser=True'))
        
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    # Cambiar username por email como campo principal
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    
    # Campos personalizados adicionales
    telefono = models.CharField(_('teléfono'), max_length=20, blank=True)
    fecha_nacimiento = models.DateField(_('fecha de nacimiento'), null=True, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    
    # Configuración para usar email como campo de identificación
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UsuarioManager()
    
    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
        db_table = 'usuarios_usuario'  # Nombre personalizado para la tabla
        
    
    def __str__(self):
        return self.email
    
    
    @property
    def tipo_usuario(self):
        """
        Devuelve el tipo de usuario como string.
        Opciones: 'mecanico', 'usuario_comun', 'admin'
        """
        if hasattr(self, 'mecanico'):
            return 'mecanico'
        elif hasattr(self, 'usuariocomun'):
            return 'usuario_comun'
        elif self.is_superuser:
            return 'admin'
        return None
    
    @property
    def es_mecanico(self):
        return self.tipo_usuario == 'mecanico'
    
    @property
    def es_usuario_comun(self):
        return self.tipo_usuario == 'usuario_comun'

    # Solución para el conflicto de related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='usuarios_usuario_set',  # Nombre único
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='usuarios_usuario_set',  # Nombre único
        related_query_name='usuario',
    )