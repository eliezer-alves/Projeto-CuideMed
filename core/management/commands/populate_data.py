from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from core.models import Usuario, Paciente, Medicamento, Prescricao, Administracao, Alerta
from datetime import date, timedelta
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo para o sistema de medicação hospitalar.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando a população do banco de dados...'))

        # 1. Criar Usuários
        self.stdout.write('Criando usuários...')
        usuarios_data = [
            {'username': 'admin', 'email': 'admin@example.com', 'password': 'adminpassword', 'tipo_usuario': 'administrador'},
            {'username': 'medico1', 'email': 'medico1@example.com', 'password': 'medpassword', 'tipo_usuario': 'medico'},
            {'username': 'enfermeiro1', 'email': 'enfermeiro1@example.com', 'password': 'enfpassword', 'tipo_usuario': 'enfermeiro'},
        ]
        for user_data in usuarios_data:
            user, created = Usuario.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'password': make_password(user_data['password']),
                    'tipo_usuario': user_data['tipo_usuario'],
                    'is_staff': True if user_data['tipo_usuario'] == 'administrador' else False,
                    'is_superuser': True if user_data['tipo_usuario'] == 'administrador' else False,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Usuário {user.username} criado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Usuário {user.username} já existe.'))
        
        admin_user = Usuario.objects.get(username='admin')
        medico_user = Usuario.objects.get(username='medico1')
        enfermeiro_user = Usuario.objects.get(username='enfermeiro1')

        # 2. Criar Pacientes
        self.stdout.write('Criando pacientes...')
        pacientes = []
        for i in range(1, 6):
            paciente, created = Paciente.objects.get_or_create(
                prontuario=f'P00{i}',
                defaults={
                    'nome': f'Paciente Teste {i}',
                    'data_nascimento': date(1980 + i, random.randint(1, 12), random.randint(1, 28)),
                    'sexo': random.choice(['M', 'F']),
                }
            )
            pacientes.append(paciente)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Paciente {paciente.nome} criado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Paciente {paciente.nome} já existe.'))

        # 3. Criar Medicamentos
        self.stdout.write('Criando medicamentos...')
        medicamentos = []
        medicamentos_data = [
            {'nome': 'Paracetamol', 'dosagem': '500mg', 'via_administracao': 'Oral'},
            {'nome': 'Dipirona', 'dosagem': '1g', 'via_administracao': 'Intravenosa'},
            {'nome': 'Amoxicilina', 'dosagem': '250mg/5ml', 'via_administracao': 'Oral'},
            {'nome': 'Morfina', 'dosagem': '10mg', 'via_administracao': 'Intramuscular'},
        ]
        for med_data in medicamentos_data:
            medicamento, created = Medicamento.objects.get_or_create(
                nome=med_data['nome'],
                dosagem=med_data['dosagem'],
                defaults={'via_administracao': med_data['via_administracao']}
            )
            medicamentos.append(medicamento)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Medicamento {medicamento.nome} criado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Medicamento {medicamento.nome} já existe.'))

        # 4. Criar Prescrições
        self.stdout.write('Criando prescrições...')
        prescricoes = []
        for paciente in pacientes:
            for medicamento in random.sample(medicamentos, 2):
                prescricao, created = Prescricao.objects.get_or_create(
                    paciente=paciente,
                    medicamento=medicamento,
                    dose=f'{random.randint(1, 2)} {medicamento.dosagem.split("/")[0].strip()}',
                    frequencia=random.choice(['6/6h', '8/8h', '12/12h']),
                    defaults={'data_hora': timezone.now() - timedelta(days=random.randint(0, 10))}
                )
                prescricoes.append(prescricao)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Prescrição para {paciente.nome} - {medicamento.nome} criada.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Prescrição para {paciente.nome} - {medicamento.nome} já existe.'))

        # 5. Criar Administrações
        self.stdout.write('Criando administrações...')
        for prescricao in prescricoes:
            if random.random() > 0.5: # Administrar cerca de metade das prescrições
                administracao, created = Administracao.objects.get_or_create(
                    prescricao=prescricao,
                    usuario=random.choice([enfermeiro_user, medico_user]),
                    defaults={'data_hora': prescricao.data_hora + timedelta(hours=random.randint(1, 24))}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Administração para {prescricao.paciente.nome} - {prescricao.medicamento.nome} registrada.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Administração para {prescricao.paciente.nome} - {prescricao.medicamento.nome} já existe.'))

        # 6. Criar Alertas
        self.stdout.write('Criando alertas...')
        for paciente in random.sample(pacientes, 3):
            alerta, created = Alerta.objects.get_or_create(
                paciente=paciente,
                tipo_alerta=random.choice(['horario', 'interacao', 'outro']),
                mensagem=f'Alerta importante para {paciente.nome} sobre {random.choice(medicamentos).nome}.',
                defaults={'data_hora': timezone.now() - timedelta(minutes=random.randint(1, 60))}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Alerta para {paciente.nome} criado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Alerta para {paciente.nome} já existe.'))

        self.stdout.write(self.style.SUCCESS('População do banco de dados concluída com sucesso!'))

