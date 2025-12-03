from rest_framework import generics, views, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from Fintrack2_api.serializers import UserRegistrationSerializer

User = get_user_model()

# Registro de Usuario
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

# Verificar si el email existe (para el frontend)
class CheckEmailView(views.APIView):
    def get(self, request):
        email = request.query_params.get('correo', None)
        if email and User.objects.filter(email=email).exists():
            return Response({'exists': True}, status=status.HTTP_200_OK)
        return Response({'exists': False}, status=status.HTTP_200_OK)
    
# --- AGREGAR ESTA NUEVA CLASE ---
class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    # Solo permitimos que un usuario logueado se edite a sí mismo
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Aseguramos que un usuario solo pueda editar su propio perfil
        return User.objects.filter(id=self.request.user.id)