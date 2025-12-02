from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets

from .models import Usuario, Paciente, Medicamento, Prescricao, Administracao, Alerta
from .serializers import (
    UsuarioSerializer, PacienteSerializer, MedicamentoSerializer,
    PrescricaoSerializer, AdministracaoSerializer, AlertaSerializer,
)

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

@login_required
@require_GET
def alertas_pendentes_api(request):
    agora = timezone.now()
    janela_futuro = agora + timedelta(minutes=5)

    print(agora, janela_futuro)

    alertas = (
        Alerta.objects.filter(
            ativo=True,
            data_hora__gte=agora,
            data_hora__lte=janela_futuro,
        )
        .select_related('paciente', 'prescricao__medicamento')
        .order_by('data_hora')
    )
    
    data = []
    for alerta in alertas:
        data.append(
            {
                "id": alerta.id,
                "paciente": alerta.paciente.nome,
                "tipo": alerta.get_tipo_alerta_display(),
                "mensagem": alerta.mensagem,
                "data_hora": alerta.data_hora.isoformat(),
                "medicamento": (
                    alerta.prescricao.medicamento.nome
                    if alerta.prescricao and alerta.prescricao.medicamento
                    else None
                ),
            }
        )

    return JsonResponse({"alertas": data})
