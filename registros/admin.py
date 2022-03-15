from django.contrib import admin
from registros.models import *

# from django.contrib.auth.admin import UserAdmin
# from .models import User

# admin.site.register(User, UserAdmin)
# # Register your models here.
admin.site.register(Bairro)
admin.site.register(TipoEntrega)
admin.site.register(Orgao)
admin.site.register(Beneficio)
admin.site.register(Beneficiado)
admin.site.register(Registro)