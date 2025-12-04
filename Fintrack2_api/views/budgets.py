from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from Fintrack2_api.models import Budget, Transaction
from Fintrack2_api.serializers import BudgetSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, 'rol', '') == 'admin':
            queryset = Budget.objects.all()
            
            target_user = self.request.query_params.get('usuario')
            categoria_id = self.request.query_params.get('categoriaId')
            
            if target_user:
                queryset = queryset.filter(user_id=target_user)
            if categoria_id:
                queryset = queryset.filter(category_id=categoria_id)
            return queryset
            
        return Budget.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff or getattr(user, 'rol', '') == 'admin':
            serializer.save()
        else:
            serializer.save(user=user)

    def perform_destroy(self, instance):
        # 1. Construimos los filtros básicos
        # Usamos 'categoria' porque así se llama el campo en tu modelo Transaction
        filters = {
            'user': instance.user,
            'categoria': instance.category.nombre 
        }

        # 2. Solo agregamos filtros de fecha SI las fechas existen (no son None)
        # Esto evita el ValueError: Cannot use None as a query value
        if instance.fecha_inicio:
            filters['fecha__gte'] = instance.fecha_inicio
        
        if instance.fecha_fin:
            filters['fecha__lte'] = instance.fecha_fin

        # 3. Ejecutamos la consulta desempaquetando los filtros (**filters)
        has_active_transactions = Transaction.objects.filter(**filters).exists()

        if has_active_transactions:
            raise ValidationError({
                'detail': '🚫 No se puede eliminar este presupuesto porque tiene transacciones registradas asociadas en este periodo. Elimine esas transacciones primero.'
            })
        
        # 4. Si pasa la validación, eliminamos
        instance.delete()