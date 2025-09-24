from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Paciente, Medicamento, Prescricao, Administracao, Alerta

class UsuarioAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (("Tipo de Usuário", {"fields": ("tipo_usuario",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Tipo de Usuário", {"fields": ("tipo_usuario",)}),)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Paciente)
admin.site.register(Medicamento)
admin.site.register(Prescricao)
admin.site.register(Administracao)
admin.site.register(Alerta)

