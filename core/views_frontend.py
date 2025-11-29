from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils import timezone
from django.views import View
from .models import Paciente, Medicamento, Prescricao, Administracao, Alerta, Usuario
from .forms import PacienteForm, MedicamentoForm, PrescricaoForm, AdministracaoForm, UsuarioLoginForm, AlertaForm, UsuarioForm, UsuarioUpdateForm

# Autenticação
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = UsuarioLoginForm

    def form_valid(self, form):
        messages.success(self.request, f'Bem-vindo, {form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Nome de usuário ou senha inválidos.')
        return super().form_invalid(form)

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Você foi desconectado com sucesso.')
        return super().dispatch(request, *args, **kwargs)

# Dashboard
class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'core/dashboard.html'
    context_object_name = 'alertas_recentes'

    def get_queryset(self):
        return Alerta.objects.order_by('-data_hora')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pacientes'] = Paciente.objects.count()
        context['total_medicamentos'] = Medicamento.objects.count()
        context['total_prescricoes_hoje'] = Prescricao.objects.filter(
            data_criacao__date=timezone.now().date()
        ).count()
        context['proximas_administracoes'] = Administracao.objects.filter(data_hora__gte=timezone.now()).order_by('data_hora')[:5]
        return context

# Paciente Views
class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'core/paciente_list.html'
    context_object_name = 'pacientes'

class PacienteDetailView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = 'core/paciente_detail.html'
    context_object_name = 'paciente'

class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'core/paciente_form.html'
    success_url = reverse_lazy('paciente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Paciente cadastrado com sucesso!')
        return super().form_valid(form)

class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'core/paciente_form.html'
    success_url = reverse_lazy('paciente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Paciente atualizado com sucesso!')
        return super().form_valid(form)

class PacienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'core/paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Paciente excluído com sucesso!')
        return super().form_valid(form)

# Medicamento Views
class MedicamentoListView(LoginRequiredMixin, ListView):
    model = Medicamento
    template_name = 'core/medicamento_list.html'
    context_object_name = 'medicamentos'

class MedicamentoCreateView(LoginRequiredMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamento_form.html'
    success_url = reverse_lazy('medicamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Medicamento cadastrado com sucesso!')
        return super().form_valid(form)

class MedicamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamento_form.html'
    success_url = reverse_lazy('medicamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Medicamento atualizado com sucesso!')
        return super().form_valid(form)

class MedicamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Medicamento
    template_name = 'core/medicamento_confirm_delete.html'
    success_url = reverse_lazy('medicamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Medicamento excluído com sucesso!')
        return super().form_valid(form)

# Prescricao Views
class PrescricaoListView(LoginRequiredMixin, ListView):
    model = Prescricao
    template_name = 'core/prescricao_list.html'
    context_object_name = 'prescricoes'

    def get_queryset(self):
        # Lista todas as prescrições, mais recentes primeiro
        return (
            Prescricao.objects
            .select_related('paciente', 'medicamento', 'medico')
            .order_by('-data_criacao')
        )

class PrescricaoCreateView(LoginRequiredMixin, CreateView):
    model = Prescricao
    form_class = PrescricaoForm
    template_name = 'core/prescricao_form.html'
    success_url = reverse_lazy('prescricao_list')

    def form_valid(self, form):
        # se o usuário logado for médico, vincula na prescrição
        if hasattr(self.request.user, 'tipo_usuario') and self.request.user.tipo_usuario == 'medico':
            form.instance.medico = self.request.user
        messages.success(self.request, 'Prescrição criada com sucesso!')
        return super().form_valid(form)

class PrescricaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Prescricao
    form_class = PrescricaoForm
    template_name = 'core/prescricao_form.html'
    success_url = reverse_lazy('prescricao_list')

    def form_valid(self, form):
        messages.success(self.request, 'Prescrição atualizada com sucesso!')
        return super().form_valid(form)

class PrescricaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Prescricao
    template_name = 'core/prescricao_confirm_delete.html'
    success_url = reverse_lazy('prescricao_list')

    def form_valid(self, form):
        messages.success(self.request, 'Prescrição excluída com sucesso!')
        return super().form_valid(form)


# class PrescricaoSuspenderView(LoginRequiredMixin, View):
#     def post(self, request, pk):
#         prescricao = get_object_or_404(Prescricao, pk=pk)
#         prescricao.status = 'suspensa'
#         prescricao.save()
#         messages.success(request, 'Prescrição suspensa com sucesso.')
#         return redirect('prescricao_list')


# Administracao Views
class AdministracaoListView(LoginRequiredMixin, ListView):
    model = Administracao
    template_name = 'core/administracao_list.html'
    context_object_name = 'administracoes'

class AdministracaoCreateView(LoginRequiredMixin, CreateView):
    model = Administracao
    form_class = AdministracaoForm
    template_name = 'core/administracao_form.html'
    success_url = reverse_lazy('administracao_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Administração registrada com sucesso!')
        return super().form_valid(form)

# Alerta Views
class AlertaListView(LoginRequiredMixin, ListView):
    model = Alerta
    template_name = 'core/alerta_list.html'
    context_object_name = 'alertas'

class AlertaCreateView(LoginRequiredMixin, CreateView):
    model = Alerta
    form_class = AlertaForm
    template_name = 'core/alerta_form.html'
    success_url = reverse_lazy('alerta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Alerta cadastrado com sucesso!')
        return super().form_valid(form)

class AlertaUpdateView(LoginRequiredMixin, UpdateView):
    model = Alerta
    form_class = AlertaForm
    template_name = 'core/alerta_form.html'
    success_url = reverse_lazy('alerta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Alerta atualizado com sucesso!')
        return super().form_valid(form)


class AlertaDeleteView(LoginRequiredMixin, DeleteView):
    model = Alerta
    template_name = 'core/alerta_confirm_delete.html'
    success_url = reverse_lazy('alerta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Alerta excluído com sucesso!')
        return super().form_valid(form)

# Usuario Views
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'core/usuario_list.html'
    context_object_name = 'usuarios'

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, 'Você não tem permissão para acessar a listagem de usuários.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'core/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário cadastrado com sucesso!')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioUpdateForm
    template_name = 'core/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, 'Você não tem permissão para editar usuários.')
            return redirect('usuario_list')
        return super().dispatch(request, *args, **kwargs)


class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'core/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário excluído com sucesso!')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, 'Você não tem permissão para excluir usuários.')
            return redirect('usuario_list')
        return super().dispatch(request, *args, **kwargs)