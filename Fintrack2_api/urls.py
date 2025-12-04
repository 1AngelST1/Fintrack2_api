from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 1. Importaciones específicas de USUARIOS 
from Fintrack2_api.views.users import RegisterView, CheckEmailView, UserUpdateView, UserListView
from Fintrack2_api.views.auth import CustomLoginView 
from Fintrack2_api.views import bootstrap 

# 2. Importaciones de las nuevas vistas separadas
from Fintrack2_api.views.categories import CategoryViewSet
from Fintrack2_api.views.transactions import TransactionViewSet
from Fintrack2_api.views.budgets import BudgetViewSet

# 3. Router para las Vistas "ViewSet"
router = DefaultRouter()
# El router ahora apunta a las clases importadas individualmente
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'budgets', BudgetViewSet, basename='budget')

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- RUTAS DE USUARIOS  
    path('api/users/register', RegisterView.as_view(), name='register'),
    path('api/users/login', CustomLoginView.as_view(), name='login'),
    path('api/users/check-email', CheckEmailView.as_view(), name='check_email'),
    path('api/users/<int:pk>', UserUpdateView.as_view(), name='user_update'),
    path('api/users/', UserListView.as_view(), name='user_list'),

    # --- RUTAS DE FINANZAS  
    path('api/', include(router.urls)),

    path('api/version', bootstrap.VersionView.as_view(), name='version'),
]