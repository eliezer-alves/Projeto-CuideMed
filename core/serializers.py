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

    class Meta:
        model = Prescricao
        fields = "__all__"

class AdministracaoSerializer(serializers.ModelSerializer):
    prescricao_detalhes = serializers.ReadOnlyField(source='prescricao.medicamento.nome')
    usuario_username = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Administracao
        fields = "__all__"

class AlertaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.ReadOnlyField(source='paciente.nome')

    class Meta:
        model = Alerta
        fields = "__all__"

