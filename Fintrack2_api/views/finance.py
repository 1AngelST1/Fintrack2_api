from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from Fintrack2_api.models import Category, Transaction, Budget
from Fintrack2_api.serializers import CategorySerializer, TransactionSerializer, BudgetSerializer
from datetime import datetime, date # Importar datetime y date

# --- VISTA DE CATEGORÍAS (Mantenida) ---
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
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                target_user = User.objects.get(pk=self.request.data['usuario'])
                serializer.save(user=target_user)
            except User.DoesNotExist:
                serializer.save(user=user)
        else:
            serializer.save(user=user)

# --- VISTA DE TRANSACCIONES (get_queryset mantenido, stats corregido) ---
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

        # Usar la misma lógica de filtrado directo que el frontend espera
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
        # --- APLICACIÓN ROBUSTA DE FILTRO DE FECHAS EN REPORTES ---
        user = self.request.user
        
        if user.is_staff or getattr(user, 'rol', '') == 'admin':
            # Si es Admin, la base es TODAS las transacciones
            queryset = Transaction.objects.all() 
        else:
            # Si NO es admin, solo ve sus propias estadísticas
            queryset = Transaction.objects.filter(user=user)
        
        # Obtener los parámetros de fecha (mapeados desde Angular)
        fecha_after_str = self.request.query_params.get('fecha_after')
        fecha_before_str = self.request.query_params.get('fecha_before')
        
        # Aplicar SÓLO los filtros de fecha con parsing robusto
        if fecha_after_str:
            try:
                # Convertimos la cadena (ej: "2025-12-01") a objeto date
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

        # Realizar la agregación
        ingresos = queryset.filter(tipo='Ingreso').aggregate(total=Sum('monto'))['total'] or 0
        gastos = queryset.filter(tipo='Gasto').aggregate(total=Sum('monto'))['total'] or 0
        
        return Response({
            'ingresos': ingresos,
            'gastos': gastos,
            'balance': ingresos - gastos
        })

# --- VISTA DE PRESUPUESTOS (Mantenida) ---
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