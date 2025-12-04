from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from Fintrack2_api.models import Transaction
from Fintrack2_api.serializers import TransactionSerializer
from datetime import datetime

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.all()
        # 1. Manejo de permisos y usuario base
        if not (user.is_staff or getattr(user, 'rol', '') == 'admin'):
            queryset = queryset.filter(user=user)
        # 2. Obtener y Aplicar Filtros (Mapeados desde Angular)
        target_user_id = self.request.query_params.get('usuario')
        fecha_after = self.request.query_params.get('fecha_after')
        fecha_before = self.request.query_params.get('fecha_before')
        tipo = self.request.query_params.get('tipo')
        categoria = self.request.query_params.get('categoria')
        limit = self.request.query_params.get('limit')

        if target_user_id:
            queryset = queryset.filter(user_id=target_user_id)

        if fecha_after:
            queryset = queryset.filter(fecha__gte=fecha_after)
        if fecha_before:
            queryset = queryset.filter(fecha__lte=fecha_before)
            
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if categoria:
            queryset = queryset.filter(categoria=categoria)

        queryset = queryset.order_by('-fecha')

        if limit:
            try:
                return queryset[:int(limit)]
            except ValueError:
                pass
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = self.request.user
        
        if user.is_staff or getattr(user, 'rol', '') == 'admin':
            queryset = Transaction.objects.all() 
        else:
            queryset = Transaction.objects.filter(user=user)
        
        fecha_after_str = self.request.query_params.get('fecha_after')
        fecha_before_str = self.request.query_params.get('fecha_before')
        
        if fecha_after_str:
            try:
                start_date = datetime.strptime(fecha_after_str, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha__gte=start_date)
            except ValueError:
                pass 
                
        if fecha_before_str:
            try:
                end_date = datetime.strptime(fecha_before_str, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha__lte=end_date)
            except ValueError:
                pass

        ingresos = queryset.filter(tipo='Ingreso').aggregate(total=Sum('monto'))['total'] or 0
        gastos = queryset.filter(tipo='Gasto').aggregate(total=Sum('monto'))['total'] or 0
        
        return Response({
            'ingresos': ingresos,
            'gastos': gastos,
            'balance': ingresos - gastos
        })