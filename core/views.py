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

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Alerta
from .forms import AlertaForm
from django.contrib.auth.mixins import LoginRequiredMixin

class AlertaCreateView(LoginRequiredMixin, CreateView):
    model = Alerta
    form_class = AlertaForm
    template_name = 'core/alerta_form.html'
    success_url = reverse_lazy('alerta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Alerta cadastrado com sucesso!')
        return super().form_valid(form)

