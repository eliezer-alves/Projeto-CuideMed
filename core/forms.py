from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Paciente, Medicamento, Prescricao, Administracao, Alerta, Usuario

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Paciente, Medicamento, Prescricao, Administracao, Alerta, Usuario


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nome',
            'cpf',
            'prontuario',
            'data_nascimento',
            'sexo',
            'telefone_contato',
            'alergias',
            'historico_clinico',
        ]
        widgets = {
            # vira <input type="date" ...>
            'data_nascimento': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'alergias': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
            'historico_clinico': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # garante bootstrap em todos os campos que não são textarea já configurado
        for name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                # evita meter form-control em checkbox/radio, se um dia tiver
                if not isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs['class'] = 'form-control'


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nome', 'dosagem', 'via_administracao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class PrescricaoForm(forms.ModelForm):
    class Meta:
        model = Prescricao
        fields = ['paciente', 'medicamento', 'dose', 'frequencia', 'status', 'observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # aplica classe bootstrap em todos
        for field in self.fields.values():
            if not isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', 'form-control')


class AdministracaoForm(forms.ModelForm):
    class Meta:
        model = Administracao
        fields = ['prescricao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prescricao'].widget.attrs.update({'class': 'form-select'})



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
        self.fields['email'].required = False
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta
        fields = [
            'tipo_alerta',
            'paciente',
            'prescricao',
            'mensagem',
            'inicio',
            'fim',
            'recorrencia',
            'hora_diaria',
            'dia_semana',
            'hora_semanal',
            'horarios_multiplos',
        ]
        widgets = {
            'mensagem': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'fim': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'hora_diaria': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'hora_semanal': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'horarios_multiplos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: 08:00,14:00,20:30',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Deixa tudo com cara de Bootstrap
        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                continue
            # Se o widget já tiver class setada em widgets, só não sobrescreve
            field.widget.attrs.setdefault('class', 'form-control')