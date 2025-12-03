from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 1. Importaciones específicas (Tu estilo solicitado)
from Fintrack2_api.views.users import RegisterView, CheckEmailView, UserUpdateView
from Fintrack2_api.views.auth import CustomLoginView  # Asegúrate que auth.py tenga esta clase
from Fintrack2_api.views import finance, bootstrap

# 2. Router para las Vistas "ViewSet" (CRUD automático de Finanzas)
# Esto maneja GET, POST, PUT, DELETE de transacciones sin escribir cada url a mano
router = DefaultRouter()
router.register(r'categories', finance.CategoryViewSet, basename='category')
router.register(r'transactions', finance.TransactionViewSet, basename='transaction')
router.register(r'budgets', finance.BudgetViewSet, basename='budget')

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- RUTAS DE USUARIOS (Tu estructura solicitada) ---
    path('api/users/register', RegisterView.as_view(), name='register'),
    path('api/users/login', CustomLoginView.as_view(), name='login'),
    path('api/users/check-email', CheckEmailView.as_view(), name='check_email'),

    # Ruta para editar perfil (Angular envía el ID, ej: api/users/2/)
    path('api/users/<int:pk>', UserUpdateView.as_view(), name='user_update'),

    # --- RUTAS DE FINANZAS (Para que funcione el Dashboard) ---
    # Esto agrega:
    #   api/transactions/
    #   api/categories/
    #   api/budgets/
    path('api/', include(router.urls)),

    # Ruta de versión (Opcional)
    path('api/version', bootstrap.VersionView.as_view(), name='version'),
]