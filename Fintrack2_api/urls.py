# Fintrack2_api/urls.py
from django.contrib import admin
from django.urls import path
from Fintrack2_api.views.users import RegisterView, CheckEmailView, UserUpdateView # <--- Importa UserUpdateView
from Fintrack2_api.views.auth import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/users/register/', RegisterView.as_view(), name='register'),
    path('api/users/login/', CustomLoginView.as_view(), name='login'),
    path('api/users/check-email/', CheckEmailView.as_view(), name='check_email'),

    # --- NUEVA RUTA PARA EDITAR PERFIL ---
    # Angular llamará a esta ruta pasando el ID del usuario
    path('api/users/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
]