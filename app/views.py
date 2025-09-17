from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Paciente, Medico, Enfermeiro, Prescricao, Medicamento, Administracao, Alerta

# ----------------------------
# Página inicial
# ----------------------------
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

# ----------------------------
# Administrações de medicamentos
# ----------------------------

# Criar nova administração
class NovaAdministracaoView(LoginRequiredMixin, CreateView):
    model = Administracao
    fields = ['prescricao_item', 'status', 'observacoes']  # campos que podem ser preenchidos no formulário
    template_name = 'nova_administracao.html'
    success_url = reverse_lazy('administracoes')

    def form_valid(self, form):
        # atribui o enfermeiro logado automaticamente (ajuste conforme seu fluxo)
        form.instance.enfermeiro = self.request.user.enfermeiro  
        return super().form_valid(form)

# Editar administração
class EditarAdministracaoView(LoginRequiredMixin, UpdateView):
    model = Administracao
    fields = ['prescricao']  # Removido 'data_hora' se for não-editável
    template_name = 'editar_administracao.html'
    success_url = reverse_lazy('administracoes')

# Deletar administração
class DeletarAdministracaoView(LoginRequiredMixin, DeleteView):
    model = Administracao
    template_name = 'deletar_administracao.html'
    success_url = reverse_lazy('administracoes')

# Listar administrações
class AdministracaoListView(View):
    def get(self, request):
        administracoes = Administracao.objects.all()
        return render(request, 'administracoes.html', {'administracoes': administracoes})

# ----------------------------
# Pacientes
# ----------------------------
class PacienteListView(View):
    def get(self, request):
        pacientes = Paciente.objects.all()
        return render(request, 'pacientes.html', {'pacientes': pacientes})

# ----------------------------
# Médicos
# ----------------------------
class MedicoListView(View):
    def get(self, request):
        medicos = Medico.objects.all()
        return render(request, 'medicos.html', {'medicos': medicos})

# ----------------------------
# Enfermeiros
# ----------------------------
class EnfermeiroListView(View):
    def get(self, request):
        enfermeiros = Enfermeiro.objects.all()
        return render(request, 'enfermeiros.html', {'enfermeiros': enfermeiros})

# ----------------------------
# Prescrições
# ----------------------------
class PrescricaoListView(View):
    def get(self, request):
        prescricoes = Prescricao.objects.all()
        return render(request, 'prescricoes.html', {'prescricoes': prescricoes})

# ----------------------------
# Medicamentos
# ----------------------------
class MedicamentoListView(View):
    def get(self, request):
        medicamentos = Medicamento.objects.all()
        return render(request, 'medicamentos.html', {'medicamentos': medicamentos})

# ----------------------------
# Alertas
# ----------------------------
class AlertaListView(View):
    def get(self, request):
        alertas = Alerta.objects.all()
        return render(request, 'alertas.html', {'alertas': alertas})
