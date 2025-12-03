from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # Importante para referenciar al usuario

# 1. MODELO DE USUARIO
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, default='usuario')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

# 2. MODELO DE CATEGORÍA
class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20) # 'Ingreso' o 'Gasto'
    estado = models.BooleanField(default=True)
    
    # Campo nuevo para el color (Hexadecimal)
    color = models.CharField(max_length=20, default='#34495e') 

    class Meta:
        unique_together = ('user', 'nombre', 'tipo')

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

# 3. MODELO DE TRANSACCIÓN
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=20)
    categoria = models.CharField(max_length=100) 
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo}: {self.monto} - {self.categoria}"

# 4. MODELO DE PRESUPUESTO
class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    periodo = models.CharField(max_length=20, default='mensual')
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Presupuesto {self.category.nombre}: {self.monto}"