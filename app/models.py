from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10)
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    historico_clinico = models.TextField()
    alergias = models.TextField(blank=True, null=True)
    restricoes_medicas = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Medicamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    data_validade = models.DateField()
    quantidade_estoque = models.PositiveIntegerField()

    def __str__(self):
        return self.nome
    

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    crm = models.CharField(max_length=20)
    especialidade = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name()

class Enfermeiro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coren = models.CharField(max_length=20)
    turno = models.CharField(max_length=20)

    def __str__(self):
        return self.user.get_full_name()

class Prescricao(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescrição de {self.paciente} por {self.medico}"

class PrescricaoItem(models.Model):
    prescricao = models.ForeignKey(Prescricao, on_delete=models.CASCADE, related_name='itens')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dose = models.CharField(max_length=50)
    frequencia = models.CharField(max_length=100)
    via = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medicamento} ({self.dose})"

class Administracao(models.Model):
    prescricao_item = models.ForeignKey(PrescricaoItem, on_delete=models.CASCADE)
    enfermeiro = models.ForeignKey(Enfermeiro, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('realizada', 'Realizada')])
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.prescricao_item} - {self.status}"

class Alerta(models.Model):
    prescricao_item = models.ForeignKey(PrescricaoItem, on_delete=models.CASCADE)
    mensagem = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return f"Alerta: {self.mensagem}"
