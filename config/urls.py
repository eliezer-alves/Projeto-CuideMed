from django.contrib import admin
from django.urls import path
from app.views import (
    IndexView,
    PacienteListView,
    MedicoListView,
    EnfermeiroListView,
    PrescricaoListView,
    MedicamentoListView,
    AdministracaoListView,
    AlertaListView,
    NovaAdministracaoView,
    EditarAdministracaoView,
    DeletarAdministracaoView,
)

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # Página inicial
    path('', IndexView.as_view(), name='index'),

    # Pacientes
    path('pacientes/', PacienteListView.as_view(), name='pacientes'),

    # Médicos
    path('medicos/', MedicoListView.as_view(), name='medicos'),

    # Enfermeiros
    path('enfermeiros/', EnfermeiroListView.as_view(), name='enfermeiros'),

    # Prescrições
    path('prescricoes/', PrescricaoListView.as_view(), name='prescricoes'),

    # Medicamentos
    path('medicamentos/', MedicamentoListView.as_view(), name='medicamentos'),

    # Administrações
    path('administracoes/', AdministracaoListView.as_view(), name='administracoes'),
    path('administracoes/nova/', NovaAdministracaoView.as_view(), name='nova_administracao'),
    path('administracoes/<int:pk>/editar/', EditarAdministracaoView.as_view(), name='editar_administracao'),
    path('administracoes/<int:pk>/deletar/', DeletarAdministracaoView.as_view(), name='deletar_administracao'),

    # Alertas
    path('alertas/', AlertaListView.as_view(), name='alertas'),
]
