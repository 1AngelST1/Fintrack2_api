from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Fintrack2_api.models import CustomUser, Category, Transaction, Budget

# 1. Configuración de USUARIOS (con la columna Rol)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'rol', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Información Extra', {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Extra', {'fields': ('rol',)}),
    )

# 2. Configuración de CATEGORÍAS
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'user', 'estado', 'color')
    list_filter = ('tipo', 'estado', 'user') # Filtros laterales
    search_fields = ('nombre', 'user__email')

# 3. Configuración de TRANSACCIONES
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'monto', 'categoria', 'fecha', 'user')
    list_filter = ('tipo', 'fecha', 'user')
    search_fields = ('descripcion', 'categoria', 'user__email')
    date_hierarchy = 'fecha' # Navegación por fechas arriba

# 4. Configuración de PRESUPUESTOS
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'monto', 'periodo')
    list_filter = ('periodo', 'user')

# --- REGISTRO DE MODELOS ---
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Budget, BudgetAdmin)