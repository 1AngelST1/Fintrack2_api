from rest_framework import serializers
from django.contrib.auth import get_user_model
from Fintrack2_api.models import Category, Transaction, Budget

# Obtenemos el modelo de usuario personalizado
User = get_user_model()

# --- SERIALIZER DE USUARIO ---
class UserRegistrationSerializer(serializers.ModelSerializer):
    # Mapeo de nombres (Frontend "nombre" -> Backend "first_name")
    nombre = serializers.CharField(source='first_name')
    apellidos = serializers.CharField(source='last_name')
    correo = serializers.EmailField(source='email')
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellidos', 'correo', 'password', 'rol']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'], # Username interno es el email
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            rol=validated_data.get('rol', 'usuario')
        )
        return user

    def update(self, instance, validated_data):
        # Actualizamos campos simples
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.rol = validated_data.get('rol', instance.rol)

        # Si viene un password nuevo, lo encriptamos y guardamos
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

# --- SERIALIZER DE CATEGORÍA ---
class CategorySerializer(serializers.ModelSerializer):
    # Mapeamos 'user' del modelo a 'usuarioId' para el frontend
    usuarioId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = Category
        # [CORRECCIÓN CRÍTICA] Agregamos 'color' aquí para que el frontend pueda enviarlo
        fields = ['id', 'nombre', 'tipo', 'estado', 'color', 'usuarioId']

# --- SERIALIZER DE TRANSACCIÓN ---
class TransactionSerializer(serializers.ModelSerializer):
    # Angular espera 'usuarioId', Django tiene 'user'
    usuarioId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    
    # Asumimos que 'categoria' en el modelo guarda el nombre (string).
    
    class Meta:
        model = Transaction
        fields = ['id', 'monto', 'tipo', 'categoria', 'descripcion', 'fecha', 'usuarioId']

# --- SERIALIZER DE PRESUPUESTO ---
class BudgetSerializer(serializers.ModelSerializer):
    usuarioId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    
    class Meta:
        model = Budget
        fields = '__all__'