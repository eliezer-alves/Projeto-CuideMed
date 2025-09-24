from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Paciente, Medicamento, Prescricao, Administracao, Usuario

class UsuarioLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nome de Usuário", widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "username"}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "current-password"}))

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nome", "data_nascimento", "sexo", "prontuario"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "sexo": forms.Select(attrs={"class": "form-select"}),
            "prontuario": forms.TextInput(attrs={"class": "form-control"}),
        }

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ["nome", "dosagem", "via_administracao"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "dosagem": forms.TextInput(attrs={"class": "form-control"}),
            "via_administracao": forms.TextInput(attrs={"class": "form-control"}),
        }

class PrescricaoForm(forms.ModelForm):
    class Meta:
        model = Prescricao
        fields = ["paciente", "medicamento", "dose", "frequencia"]
        widgets = {
            "paciente": forms.Select(attrs={"class": "form-select"}),
            "medicamento": forms.Select(attrs={"class": "form-select"}),
            "dose": forms.TextInput(attrs={"class": "form-control"}),
            "frequencia": forms.TextInput(attrs={"class": "form-control"}),
        }

class AdministracaoForm(forms.ModelForm):
    class Meta:
        model = Administracao
        fields = ["prescricao"]
        widgets = {
            "prescricao": forms.Select(attrs={"class": "form-select"}),
        }

