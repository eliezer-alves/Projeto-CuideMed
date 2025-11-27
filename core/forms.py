from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Paciente, Medicamento, Prescricao, Administracao, Alerta, Usuario

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

# Formulário de cadastro de usuário (somente para admins)
class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})