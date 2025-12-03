from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 1. IMPORTANTE: Agregamos UserListView a los imports
from Fintrack2_api.views.users import RegisterView, CheckEmailView, UserUpdateView, UserListView
from Fintrack2_api.views.auth import CustomLoginView
from Fintrack2_api.views import finance, bootstrap

# 2. Router para las Vistas "ViewSet" (CRUD automático de Finanzas)
router = DefaultRouter()
router.register(r'categories', finance.CategoryViewSet, basename='category')
router.register(r'transactions', finance.TransactionViewSet, basename='transaction')
router.register(r'budgets', finance.BudgetViewSet, basename='budget')

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- RUTAS DE USUARIOS ---
    path('api/users/register', RegisterView.as_view(), name='register'),
    path('api/users/login', CustomLoginView.as_view(), name='login'),
    path('api/users/check-email', CheckEmailView.as_view(), name='check_email'),

    # Ruta para editar perfil
    path('api/users/<int:pk>', UserUpdateView.as_view(), name='user_update'),

    # --- NUEVA RUTA (SOLUCIÓN ERROR 404) ---
    # Esta ruta captura "api/users/" y muestra la lista
    path('api/users/', UserListView.as_view(), name='user_list'),

    # --- RUTAS DE FINANZAS ---
    path('api/', include(router.urls)),

    # Ruta de versión
    path('api/version', bootstrap.VersionView.as_view(), name='version'),
]