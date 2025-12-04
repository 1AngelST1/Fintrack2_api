from rest_framework import serializers
from django.contrib.auth import get_user_model
from Fintrack2_api.models import Category, Transaction, Budget
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()

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


class TransactionSerializer(serializers.ModelSerializer):
 
    usuarioId = serializers.PrimaryKeyRelatedField(
        source='user', 
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Transaction
        fields = ['id', 'monto', 'tipo', 'categoria', 'descripcion', 'fecha', 'usuarioId']

class BudgetSerializer(serializers.ModelSerializer):
    # Campos definidos explícitamente
    usuarioId = serializers.PrimaryKeyRelatedField(
        source='user', 
        queryset=User.objects.all()
    )
    categoriaId = serializers.PrimaryKeyRelatedField(
        source='category', 
        queryset=Category.objects.all()
    )
    
    categoria = serializers.CharField(source='category.nombre', read_only=True)

    class Meta:
        model = Budget
        fields = ['id', 'usuarioId', 'categoriaId', 'categoria', 'monto', 'periodo']
        
        # CORRECCIÓN: Los nombres aquí deben coincidir con los campos del SERIALIZADOR
        validators = [
            UniqueTogetherValidator(
                queryset=Budget.objects.all(),
                fields=['usuarioId', 'categoriaId'], # <--- CAMBIO: Usar nombres del serializador
                message="Ya existe un presupuesto configurado para esta categoría."
            )
        ]