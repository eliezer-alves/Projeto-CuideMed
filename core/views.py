from rest_framework import viewsets
from .models import Usuario, Paciente, Medicamento, Prescricao, Administracao, Alerta
from .serializers import UsuarioSerializer, PacienteSerializer, MedicamentoSerializer, PrescricaoSerializer, AdministracaoSerializer, AlertaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

class PrescricaoViewSet(viewsets.ModelViewSet):
    queryset = Prescricao.objects.all()
    serializer_class = PrescricaoSerializer

class AdministracaoViewSet(viewsets.ModelViewSet):
    queryset = Administracao.objects.all()
    serializer_class = AdministracaoSerializer

class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer

