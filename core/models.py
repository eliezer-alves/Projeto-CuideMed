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
        self.is_staff = self.tipo_usuario == 'administrador'
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

    RECORRENCIA_CHOICES = [
        ('nenhuma', 'Sem recorrência'),
        ('diaria', 'Diariamente em um horário'),
        ('semanal', 'Semanalmente em um dia e horário'),
        ('varias_vezes_dia', 'Várias vezes ao dia'),
    ]

    DIAS_SEMANA = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    # ————— Tipo e alvo do alerta —————
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

    prescricao = models.ForeignKey(
        Prescricao,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alertas',
    )

    mensagem = models.TextField()

    # ————— Janela de atividade —————
    inicio = models.DateTimeField(default=timezone.now)
    fim = models.DateTimeField(null=True, blank=True)

    # ————— Recorrência —————
    recorrencia = models.CharField(
        max_length=20,
        choices=RECORRENCIA_CHOICES,
        default='nenhuma',
    )

    # Se diária → um horário fixo no dia
    hora_diaria = models.TimeField(
        null=True,
        blank=True,
        help_text="Usado quando a recorrência é diária.",
    )

    # Se semanal → dia da semana + horário
    dia_semana = models.IntegerField(
        choices=DIAS_SEMANA,
        null=True,
        blank=True,
        help_text="Usado quando a recorrência é semanal.",
    )
    hora_semanal = models.TimeField(
        null=True,
        blank=True,
        help_text="Usado quando a recorrência é semanal.",
    )

    # Se várias vezes ao dia → lista de horários HH:MM separados por vírgula
    horarios_multiplos = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Quando for várias vezes ao dia, informe horários no formato HH:MM separados por vírgula (ex: 08:00,14:00,20:30).",
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"

    def __str__(self):
        if self.tipo_alerta == 'prescricao' and self.prescricao:
            return f"Alerta de prescrição ({self.prescricao})"
        return f"Alerta para {self.paciente.nome}"

    def clean(self):
        """
        Valida as combinações tipo_alerta + recorrência + campos auxiliares.
        Mantém as regras simples, mas já garante consistência.
        """
        super().clean()

        # Se for alerta de prescrição, precisa ter prescricao associada
        if self.tipo_alerta == 'prescricao' and not self.prescricao:
            raise ValidationError("Alertas do tipo 'prescrição' devem estar vinculados a uma prescrição.")

        # Garante paciente vindo da prescrição quando existir
        if self.tipo_alerta == 'prescricao' and self.prescricao:
            self.paciente = self.prescricao.paciente

        # Reset de campos que não fazem sentido para determinadas recorrências
        if self.recorrencia == 'nenhuma':
            self.hora_diaria = None
            self.dia_semana = None
            self.hora_semanal = None
            self.horarios_multiplos = None

        elif self.recorrencia == 'diaria':
            if not self.hora_diaria:
                raise ValidationError("Para recorrência diária, informe o horário diário do alerta.")
            # limpa outros
            self.dia_semana = None
            self.hora_semanal = None
            self.horarios_multiplos = None

        elif self.recorrencia == 'semanal':
            if self.dia_semana is None or not self.hora_semanal:
                raise ValidationError("Para recorrência semanal, informe o dia da semana e o horário.")
            # limpa outros
            self.hora_diaria = None
            self.horarios_multiplos = None

        elif self.recorrencia == 'varias_vezes_dia':
            if not self.horarios_multiplos:
                raise ValidationError("Para recorrência 'várias vezes ao dia', informe ao menos um horário.")
            # valida formato básico HH:MM,HH:MM…
            partes = [p.strip() for p in self.horarios_multiplos.split(',') if p.strip()]
            from datetime import time
            for p in partes:
                try:
                    h, m = p.split(':')
                    h = int(h)
                    m = int(m)
                    time(hour=h, minute=m)
                except Exception:
                    raise ValidationError(
                        "Use horários no formato HH:MM separados por vírgula, por exemplo: 08:00,14:00,20:30."
                    )
            # limpa campos não usados
            self.hora_diaria = None
            self.dia_semana = None
            self.hora_semanal = None


