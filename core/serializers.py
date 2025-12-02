from rest_framework import serializers
from .models import Usuario, Paciente, Medicamento, Prescricao, Administracao, Alerta


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "username", "email", "tipo_usuario"]


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = "__all__"


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = "__all__"


class PrescricaoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.ReadOnlyField(source='paciente.nome')
    medicamento_nome = serializers.ReadOnlyField(source='medicamento.nome')
    medico_username = serializers.ReadOnlyField(source='medico.username')

    class Meta:
        model = Prescricao
        fields = "__all__"  # inclui todos os campos do model + os extras declarados acima


class AdministracaoSerializer(serializers.ModelSerializer):
    prescricao_medicamento = serializers.ReadOnlyField(source='prescricao.medicamento.nome')
    paciente_nome = serializers.ReadOnlyField(source='prescricao.paciente.nome')
    usuario_username = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Administracao
        fields = "__all__"


class AlertaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.ReadOnlyField(source='paciente.nome')
    tipo_alerta_display = serializers.CharField(source='get_tipo_alerta_display', read_only=True)
    medicamento_nome = serializers.SerializerMethodField()

    class Meta:
        model = Alerta
        fields = "__all__"

    def get_medicamento_nome(self, obj):
        if obj.prescricao and obj.prescricao.medicamento:
            return obj.prescricao.medicamento.nome
        return None
