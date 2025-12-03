from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Angular envía 'correo', Django espera 'username'
        data = request.data.copy()
        if 'correo' in data:
            data['username'] = data['correo']
        
        serializer = self.serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Respuesta personalizada para Angular
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'nombre': user.first_name,
                'apellidos': user.last_name,
                'correo': user.email,
                'rol': getattr(user, 'rol', 'usuario')
            }
        })