from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Fintrack2_api.models import CustomUser

# Registramos el nuevo modelo de usuario
# Usamos UserAdmin para que Django sepa cómo manejar passwords en el panel
admin.site.register(CustomUser, UserAdmin)