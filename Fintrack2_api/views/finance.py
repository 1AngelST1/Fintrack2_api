from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from Fintrack2_api.models import Category, Transaction, Budget
from Fintrack2_api.serializers import CategorySerializer, TransactionSerializer, BudgetSerializer

# --- VISTA DE CATEGORÍAS ---
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.all()

        if user.is_staff or getattr(user, 'rol', '') == 'admin':
            usuario_id = self.request.query_params.get('usuarioId')
            if usuario_id:
                queryset = queryset.filter(user_id=usuario_id)
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
        # Lógica para permitir al admin crear categorías para otros
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

# --- VISTA DE TRANSACCIONES ---
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff or getattr(user, 'rol', '') == 'admin':
            queryset = Transaction.objects.all()
            target_user_id = self.request.query_params.get('usuarioId')
            if target_user_id:
                queryset = queryset.filter(user_id=target_user_id)
        else:
            queryset = Transaction.objects.filter(user=user)
        
        fecha_desde = self.request.query_params.get('fechaDesde')
        fecha_hasta = self.request.query_params.get('fechaHasta')
        tipo = self.request.query_params.get('tipo')
        categoria = self.request.query_params.get('categoria')
        limit = self.request.query_params.get('limit')

        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)
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
        # Si TransactionSerializer ya maneja usuarioId (como read_only), aquí forzamos el usuario
        # O permitimos admin override si modificas el serializer en el futuro
        serializer.save(user=user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        ingresos = queryset.filter(tipo='Ingreso').aggregate(total=Sum('monto'))['total'] or 0
        gastos = queryset.filter(tipo='Gasto').aggregate(total=Sum('monto'))['total'] or 0
        
        return Response({
            'ingresos': ingresos,
            'gastos': gastos,
            'balance': ingresos - gastos
        })

# --- VISTA DE PRESUPUESTOS (CORREGIDA) ---
class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, 'rol', '') == 'admin':
            queryset = Budget.objects.all()
            target_user = self.request.query_params.get('usuarioId')
            categoria_id = self.request.query_params.get('categoriaId')
            
            if target_user:
                queryset = queryset.filter(user_id=target_user)
            if categoria_id:
                queryset = queryset.filter(category_id=categoria_id)
            return queryset
            
        return Budget.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        # Si es admin, respetamos el usuarioId que viene en el serializer
        if user.is_staff or getattr(user, 'rol', '') == 'admin':
            serializer.save()
        else:
            # Si es usuario normal, forzamos que sea suyo (por seguridad)
            serializer.save(user=user)