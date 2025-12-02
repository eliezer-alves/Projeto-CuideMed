from datetime import timedelta

from django.utils import timezone

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Usuario, Paciente, Medicamento, Prescricao, Administracao, Alerta
from .serializers import (
    UsuarioSerializer,
    PacienteSerializer,
    MedicamentoSerializer,
    PrescricaoSerializer,
    AdministracaoSerializer,
    AlertaSerializer,
)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [permissions.IsAuthenticated]


class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrescricaoViewSet(viewsets.ModelViewSet):
    queryset = Prescricao.objects.all()
    serializer_class = PrescricaoSerializer
    permission_classes = [permissions.IsAuthenticated]


class AdministracaoViewSet(viewsets.ModelViewSet):
    queryset = Administracao.objects.all()
    serializer_class = AdministracaoSerializer
    permission_classes = [permissions.IsAuthenticated]


class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    permission_classes = [permissions.IsAuthenticated]


class AlertasPendentesAPIView(APIView):
    """
    Retorna alertas ativos cujo horário está dentro da janela dos próximos 5 minutos.

    Usado pelo frontend para mostrar badge/modal de alertas pendentes.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        agora = timezone.now()
        janela_futuro = agora + timedelta(minutes=5)

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

        return Response({"alertas": data})
