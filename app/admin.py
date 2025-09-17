from django.contrib import admin
from .models import *

class PrescricaoItemInline(admin.TabularInline):
    model = PrescricaoItem
    extra = 1

class PrescricaoAdmin(admin.ModelAdmin):
    inlines = [PrescricaoItemInline]

admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Enfermeiro)
admin.site.register(Medicamento)
admin.site.register(Prescricao, PrescricaoAdmin)
admin.site.register(Administracao)
admin.site.register(Alerta)
