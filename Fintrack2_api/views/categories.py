from rest_framework import viewsets, permissions
from Fintrack2_api.models import Category
from Fintrack2_api.serializers import CategorySerializer
from django.contrib.auth import get_user_model # Necesario para perform_create

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.all()
        if user.is_staff or getattr(user, 'rol', '') == 'admin':
            target_user_id = self.request.query_params.get('usuario') 
            if target_user_id:
                queryset = queryset.filter(user_id=target_user_id)
        else:
            queryset = queryset.filter(user=user)
            
        tipo = self.request.query_params.get('tipo')
        nombre = self.request.query_params.get('nombre')
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        if (user.is_staff or getattr(user, 'rol', '') == 'admin') and 'usuario' in self.request.data:
            User = get_user_model()
            try:
                target_user = User.objects.get(pk=self.request.data['usuario'])
                serializer.save(user=target_user)
            except User.DoesNotExist:
                serializer.save(user=user)
        else:
            serializer.save(user=user)