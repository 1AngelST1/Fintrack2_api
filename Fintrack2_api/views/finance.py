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

        # Si es Admin, permitir filtrar por usuarioId específico
        if user.is_staff or getattr(user, 'rol', '') == 'admin':
            usuario_id = self.request.query_params.get('usuarioId')
            if usuario_id:
                queryset = queryset.filter(user_id=usuario_id)
            else:
                # Si es admin pero no filtra, ve todas (o puedes restringir a las suyas)
                pass 
        else:
            # Usuario normal solo ve las suyas
            queryset = queryset.filter(user=user)
            
        # Filtros adicionales
        tipo = self.request.query_params.get('tipo')
        nombre = self.request.query_params.get('nombre')
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)

        return queryset

    def perform_create(self, serializer):
        # Si es admin y envía un usuarioId en el body (manejado en serializer) o URL
        # Por defecto, asignamos al usuario actual si no se especifica otro lógica
        serializer.save(user=self.request.user)

# --- VISTA DE TRANSACCIONES ---
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # 1. Lógica base: ¿Quién pide los datos?
        if user.is_staff or getattr(user, 'rol', '') == 'admin':
            queryset = Transaction.objects.all()
            # Admin puede filtrar por usuarioId
            target_user_id = self.request.query_params.get('usuarioId')
            if target_user_id:
                queryset = queryset.filter(user_id=target_user_id)
        else:
            # Usuario normal: SOLO sus datos
            queryset = Transaction.objects.filter(user=user)
        
        # 2. Obtener parámetros de la URL
        fecha_desde = self.request.query_params.get('fechaDesde')
        fecha_hasta = self.request.query_params.get('fechaHasta')
        tipo = self.request.query_params.get('tipo')          # Faltaba esto
        categoria = self.request.query_params.get('categoria') # Faltaba esto
        limit = self.request.query_params.get('limit')

        # 3. Aplicar Filtros
        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if categoria:
            queryset = queryset.filter(categoria=categoria)

        # 4. Ordenamiento
        queryset = queryset.order_by('-fecha')

        # 5. Limitar resultados (para dashboard)
        if limit:
            try:
                return queryset[:int(limit)]
            except ValueError:
                pass
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        
        # Si es Admin y el frontend manda un usuarioId, el serializer debería manejarlo
        # Si tu TransactionSerializer tiene 'usuarioId' como read_only, 
        # aquí deberíamos inyectar el ID si viene en el request.data
        
        if (user.is_staff or getattr(user, 'rol', '') == 'admin') and 'usuarioId' in self.request.data:
             # Ojo: esto requiere importar el modelo User o usar get_user_model()
             from django.contrib.auth import get_user_model
             User = get_user_model()
             target_user = User.objects.get(pk=self.request.data['usuarioId'])
             serializer.save(user=target_user)
        else:
            serializer.save(user=user)

    # --- ACCIÓN EXTRA: Calcular Balance ---
    @action(detail=False, methods=['get'])
    def stats(self, request):
        # Reutilizamos la lógica de filtrado para que las stats coincidan con los filtros
        queryset = self.filter_queryset(self.get_queryset())

        # Calculamos las sumas directo en la BD
        ingresos = queryset.filter(tipo='Ingreso').aggregate(total=Sum('monto'))['total'] or 0
        gastos = queryset.filter(tipo='Gasto').aggregate(total=Sum('monto'))['total'] or 0
        
        # Nota: Asegúrate que en tu BD el tipo se guarde como 'Ingreso'/'Gasto' (Title Case) 
        # o 'ingreso'/'gasto' (lowercase) y ajusta las líneas de arriba.
        
        return Response({
            'ingresos': ingresos,
            'gastos': gastos,
            'balance': ingresos - gastos
        })

# --- VISTA DE PRESUPUESTOS ---
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
        serializer.save(user=self.request.user)