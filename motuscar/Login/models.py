from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'custom_user'  # Nombre personalizado para la tabla

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="customuser_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="customuser_permissions",
        blank=True,
    )