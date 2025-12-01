from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError

class Usuario(AbstractUser):
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    TIPO_USUARIO_CHOICES = [
        ('medico', 'Médico'),
        ('enfermeiro', 'Enfermeiro'),
        ('administrador', 'Administrador'),
    ]
    tipo_usuario = models.CharField(max_length=15, choices=TIPO_USUARIO_CHOICES, default='enfermeiro')

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username
    
def save(self, *args, **kwargs):
    if self.is_superuser:
        self.is_staff = True
    else:
        self.is_staff = (self.tipo_usuario == "administrador")
    super().save(*args, **kwargs)

class Paciente(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    prontuario = models.CharField(max_length=50, unique=True)
    telefone_contato = models.CharField(max_length=20, blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    historico_clinico = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return self.nome

class Medicamento(models.Model):
    nome = models.CharField(max_length=255)
    dosagem = models.CharField(max_length=100)
    via_administracao = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"

    def __str__(self):
        return f"{self.nome} ({self.dosagem})"

class Prescricao(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('suspensa', 'Suspensa'),
        ('encerrada', 'Encerrada'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)

    # médico que prescreveu (usuário logado do tipo médico)
    medico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='prescricoes',
        null=True,
        blank=True,
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ultima_atualizacao = models.DateTimeField(auto_now=True)

    dose = models.CharField(max_length=100)
    frequencia = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ativa',
    )

    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Prescrição"
        verbose_name_plural = "Prescrições"

    def __str__(self):
        return f"Prescrição para {self.paciente.nome} - {self.medicamento.nome}"

    def get_status_badge_class(self):
        mapping = {
            'ativa': 'bg-success',     # verde
            'suspensa': 'bg-warning',  # amarelo
            'encerrada': 'bg-secondary',  # cinza
        }
        # badge padrão se cair em algum status inesperado
        return mapping.get(self.status, 'bg-secondary')

class Administracao(models.Model):
    prescricao = models.ForeignKey(Prescricao, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Administração"
        verbose_name_plural = "Administrações"

    def __str__(self):
        return f"Administração de {self.prescricao.medicamento.nome} por {self.usuario.username}"

class Alerta(models.Model):
    TIPO_ALERTA_CHOICES = [
        ('prescricao', 'Relacionado à prescrição'),
        ('outro', 'Outro alerta clínico'),
    ]

    INTERVALO_CHOICES = [
        ('4h', 'A cada 4 horas'),
        ('6h', 'A cada 6 horas'),
        ('8h', 'A cada 8 horas'),
        ('12h', 'A cada 12 horas'),
        ('24h', 'A cada 24 horas'),
        ('semanal', 'Uma vez por semana'),
    ]

    tipo_alerta = models.CharField(
        max_length=20,
        choices=TIPO_ALERTA_CHOICES,
        default='prescricao',
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='alertas',
    )

    # Se for alerta ligado a uma prescrição
    prescricao = models.ForeignKey(
        Prescricao,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alertas',
    )

    mensagem = models.TextField()

    # Quando o alerta deve disparar (primeira ocorrência)
    data_hora = models.DateTimeField(default=timezone.now)

    # Se vai repetir ou não
    repetir = models.BooleanField(default=False)

    # Intervalo da repetição (se repetir=True)
    repetir_intervalo = models.CharField(
        max_length=20,
        choices=INTERVALO_CHOICES,
        blank=True,
        null=True,
    )

    # Ativo / Inativo (status do alerta)
    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"

    def __str__(self):
        if self.tipo_alerta == 'prescricao' and self.prescricao:
            return f"Alerta de prescrição ({self.prescricao})"
        return f"Alerta para {self.paciente.nome}"