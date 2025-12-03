from django.db import models
from django.contrib.auth.models import AbstractUser

# Si ya tienes otros modelos aquí, pon este al principio
class CustomUser(AbstractUser):
    # Usamos email como identificador principal
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, default='usuario')
    
    # Configuraciones de Django para usar email en lugar de username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email