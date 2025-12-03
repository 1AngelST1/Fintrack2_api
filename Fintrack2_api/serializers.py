from rest_framework import serializers
from django.contrib.auth import get_user_model
from Fintrack2_api.models import Category, Transaction, Budget

User = get_user_model()

# ... (UserRegistrationSerializer y CategorySerializer se mantienen igual) ...
class UserRegistrationSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='first_name')
    apellidos = serializers.CharField(source='last_name')
    correo = serializers.EmailField(source='email')
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellidos', 'correo', 'password', 'rol']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            rol=validated_data.get('rol', 'usuario')
        )
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.rol = validated_data.get('rol', instance.rol)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    usuarioId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'nombre', 'tipo', 'estado', 'color', 'usuarioId']

# --- SERIALIZER DE TRANSACCIÓN (ACTUALIZADO) ---
class TransactionSerializer(serializers.ModelSerializer):
    # Habilitamos escritura para 'usuarioId'
    usuarioId = serializers.PrimaryKeyRelatedField(
        source='user', 
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Transaction
        fields = ['id', 'monto', 'tipo', 'categoria', 'descripcion', 'fecha', 'usuarioId']

# --- SERIALIZER DE PRESUPUESTO ---
class BudgetSerializer(serializers.ModelSerializer):
    usuarioId = serializers.PrimaryKeyRelatedField(
        source='user', 
        queryset=User.objects.all()
    )
    categoriaId = serializers.PrimaryKeyRelatedField(
        source='category', 
        queryset=Category.objects.all()
    )
    
    # Renombramos 'categoria_nombre' a 'categoria' para coincidir con el front
    categoria = serializers.CharField(source='category.nombre', read_only=True)

    class Meta:
        model = Budget
        fields = ['id', 'usuarioId', 'categoriaId', 'categoria', 'monto', 'periodo']