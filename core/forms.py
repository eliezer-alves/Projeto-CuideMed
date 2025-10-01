from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Paciente, Medicamento, Prescricao, Administracao, Alerta

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento', 'sexo', 'prontuario']

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nome', 'dosagem', 'via_administracao']

class PrescricaoForm(forms.ModelForm):
    class Meta:
        model = Prescricao
        fields = ['paciente', 'medicamento', 'dose', 'frequencia']

class AdministracaoForm(forms.ModelForm):
    class Meta:
        model = Administracao
        fields = ['prescricao']

# ✅ Formulário para criar alertas
class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta
        fields = ['paciente', 'medicamento', 'tipo_alerta', 'mensagem']

# Formulário de login personalizado
class UsuarioLoginForm(AuthenticationForm):
    pass
