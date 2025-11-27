from django.db import models
from django.contrib.auth.models import AbstractUser

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
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    prontuario = models.CharField(max_length=50, unique=True)

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
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    dose = models.CharField(max_length=100)
    frequencia = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Prescrição"
        verbose_name_plural = "Prescrições"

    def __str__(self):
        return f"Prescrição para {self.paciente.nome} - {self.medicamento.nome}"

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
        ('horario', 'Horário de Medicação'),
        ('interacao', 'Interação Medicamentosa'),
        ('outro', 'Outro'),
    ]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medicamento = models.CharField(max_length=255, blank=True, null=True) # Pode ser uma lista de medicamentos ou um único
    tipo_alerta = models.CharField(max_length=20, choices=TIPO_ALERTA_CHOICES)
    mensagem = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"

    def __str__(self):
        return f"Alerta para {self.paciente.nome} - {self.tipo_alerta}"

