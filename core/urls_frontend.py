from django.urls import path
from .views_frontend import (
    CustomLoginView, CustomLogoutView, DashboardView,
    PacienteListView, PacienteDetailView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView,
    MedicamentoListView, MedicamentoCreateView, MedicamentoUpdateView, MedicamentoDeleteView,
    PrescricaoListView, PrescricaoCreateView,
    AdministracaoListView, AdministracaoCreateView,
    AlertaListView, AlertaCreateView,
    UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView,
)

urlpatterns = [
    # Autenticação
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Pacientes
    path('pacientes/', PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/<int:pk>/', PacienteDetailView.as_view(), name='paciente_detail'),
    path('pacientes/novo/', PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/<int:pk>/editar/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/<int:pk>/excluir/', PacienteDeleteView.as_view(), name='paciente_delete'),
    
    # Medicamentos
    path('medicamentos/', MedicamentoListView.as_view(), name='medicamento_list'),
    path('medicamentos/novo/', MedicamentoCreateView.as_view(), name='medicamento_create'),
    path('medicamentos/<int:pk>/editar/', MedicamentoUpdateView.as_view(), name='medicamento_update'),
    path('medicamentos/<int:pk>/excluir/', MedicamentoDeleteView.as_view(), name='medicamento_delete'),
    
    # Prescrições
    path('prescricoes/', PrescricaoListView.as_view(), name='prescricao_list'),
    path('prescricoes/nova/', PrescricaoCreateView.as_view(), name='prescricao_create'),
    
    # Administrações
    path('administracoes/', AdministracaoListView.as_view(), name='administracao_list'),
    path('administracoes/nova/', AdministracaoCreateView.as_view(), name='administracao_create'),
    
    # Alertas
    path('alertas/', AlertaListView.as_view(), name='alerta_list'),
    path('alertas/adicionar/', AlertaCreateView.as_view(), name='alerta_add'),

    # Usuários
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/novo/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/<int:pk>/excluir/', UsuarioDeleteView.as_view(), name='usuario_delete'),
]
