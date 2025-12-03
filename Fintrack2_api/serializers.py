from rest_framework import serializers
from django.contrib.auth import get_user_model

# Obtenemos el modelo de usuario que definimos arriba
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Mapeo de nombres (Frontend -> Backend)
    nombre = serializers.CharField(source='first_name')
    apellidos = serializers.CharField(source='last_name')
    correo = serializers.EmailField(source='email')
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellidos', 'correo', 'password', 'rol']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'], # Username interno = email
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

        # Si viene un password nuevo, lo encriptamos y guardamos
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance