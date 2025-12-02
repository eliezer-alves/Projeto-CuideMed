import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import (
    Usuario,
    Paciente,
    Medicamento,
    Prescricao,
    Administracao,
    Alerta,
)


class Command(BaseCommand):
    help = "Cria dados de exemplo (seeds) para a aplicação de medicação hospitalar."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Iniciando seed de dados de exemplo..."))

        admin_user, medico_user, enfermeiro_user = self._create_users()
        self.stdout.write(self.style.SUCCESS("✔ Usuários de exemplo criados."))

        pacientes = self._create_pacientes()
        self.stdout.write(self.style.SUCCESS(f"✔ {len(pacientes)} pacientes criados/recuperados."))

        medicamentos = self._create_medicamentos()
        self.stdout.write(self.style.SUCCESS(f"✔ {len(medicamentos)} medicamentos criados/recuperados."))

        prescricoes = self._create_prescricoes(pacientes, medicamentos, medico_user)
        self.stdout.write(self.style.SUCCESS(f"✔ {len(prescricoes)} prescrições criadas."))

        administracoes = self._create_administracoes(prescricoes, medico_user, enfermeiro_user)
        self.stdout.write(self.style.SUCCESS(f"✔ {len(administracoes)} administrações criadas."))

        alertas = self._create_alertas(pacientes, prescricoes)
        self.stdout.write(self.style.SUCCESS(f"✔ {len(alertas)} alertas criados."))

        self.stdout.write(self.style.SUCCESS("Seed concluído com sucesso."))

    # -----------------------------
    # Helpers
    # -----------------------------

    def _create_users(self):
        """
        Cria 3 usuários básicos:
        - admin (superuser)
        - medico
        - enfermeiro
        Senha padrão: 123456
        """

        admin_user, _ = Usuario.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "tipo_usuario": "administrador",
                "is_superuser": True,
                "is_staff": True,
            },
        )
        if not admin_user.password:
            admin_user.set_password("123456")
            admin_user.save()

        medico_user, _ = Usuario.objects.get_or_create(
            username="medico_demo",
            defaults={
                "email": "medico@example.com",
                "tipo_usuario": "medico",
            },
        )
        if not medico_user.password:
            medico_user.set_password("123456")
            medico_user.save()

        enfermeiro_user, _ = Usuario.objects.get_or_create(
            username="enfermeiro_demo",
            defaults={
                "email": "enfermeiro@example.com",
                "tipo_usuario": "enfermeiro",
            },
        )
        if not enfermeiro_user.password:
            enfermeiro_user.set_password("123456")
            enfermeiro_user.save()

        return admin_user, medico_user, enfermeiro_user

    def _create_pacientes(self):
        nomes_base = [
            "Ana Souza",
            "Bruno Lima",
            "Carlos Silva",
            "Daniela Costa",
            "Eduardo Pereira",
            "Fernanda Rocha",
            "Gabriel Martins",
            "Helena Santos",
            "Igor Almeida",
            "Julia Ribeiro",
            "Karen Oliveira",
            "Lucas Ferreira",
            "Mariana Gomes",
            "Nicolas Araujo",
            "Olivia Mendes",
            "Paulo Henrique",
            "Rafaela Moreira",
            "Tiago Carvalho",
            "Valeria Nunes",
            "Wesley Campos",
        ]

        pacientes = []
        base_date = date(1980, 1, 1)

        for idx, nome in enumerate(nomes_base, start=1):
            prontuario = f"P{idx:04d}"
            cpf = f"{10000000000 + idx}"

            paciente, _ = Paciente.objects.get_or_create(
                prontuario=prontuario,
                defaults={
                    "nome": nome,
                    "cpf": cpf,
                    "data_nascimento": base_date + timedelta(days=idx * 365 // 2),
                    "sexo": random.choice(["M", "F", "O"]),
                    "telefone_contato": f"(35) 9{9000 + idx:04d}-{1000 + idx:04d}",
                    "alergias": "Sem alergias conhecidas.",
                    "historico_clinico": "Paciente sem histórico clínico relevante para este ambiente de teste.",
                },
            )
            pacientes.append(paciente)

        return pacientes

    def _create_medicamentos(self):
        medicamentos_def = [
            ("Dipirona", "500 mg", "VO"),
            ("Paracetamol", "750 mg", "VO"),
            ("Ibuprofeno", "600 mg", "VO"),
            ("Amoxicilina", "500 mg", "VO"),
            ("Azitromicina", "500 mg", "VO"),
            ("Omeprazol", "20 mg", "VO"),
            ("Metformina", "850 mg", "VO"),
            ("Losartana", "50 mg", "VO"),
            ("Hidroclorotiazida", "25 mg", "VO"),
            ("Enalapril", "10 mg", "VO"),
            ("Captopril", "25 mg", "VO"),
            ("Atorvastatina", "20 mg", "VO"),
            ("Sinvastatina", "20 mg", "VO"),
            ("Insulina Regular", "UI conforme prescrição", "SC"),
            ("Insulina NPH", "UI conforme prescrição", "SC"),
            ("Heparina", "5.000 UI", "SC"),
            ("Ceftriaxona", "1 g", "IV"),
            ("Vancomicina", "1 g", "IV"),
            ("Metronidazol", "500 mg", "IV"),
            ("Furosemida", "40 mg", "IV"),
            ("Morfina", "5 mg", "IV"),
            ("Tramadol", "50 mg", "IV"),
            ("Ondansetrona", "8 mg", "IV"),
            ("Clorpromazina", "25 mg", "VO"),
            ("Sertralina", "50 mg", "VO"),
            ("Diazepam", "10 mg", "VO"),
            ("Haloperidol", "5 mg", "IM"),
            ("Adrenalina", "1 mg", "IV"),
            ("Noradrenalina", "4 mg em SG 5%", "IV"),
            ("Salbutamol", "100 mcg", "Inalatória"),
        ]

        medicamentos = []

        for nome, dosagem, via in medicamentos_def:
            med, _ = Medicamento.objects.get_or_create(
                nome=nome,
                dosagem=dosagem,
                via_administracao=via,
            )
            medicamentos.append(med)

        return medicamentos

    def _create_prescricoes(self, pacientes, medicamentos, medico_user):
        descricoes_dose = [
            "1 comprimido",
            "1 comprimido e meio",
            "2 comprimidos",
            "10 gotas",
            "1 ampola",
        ]
        frequencias = [
            "8/8h",
            "12/12h",
            "24/24h",
            "6/6h se dor",
            "1x ao dia",
        ]
        observacoes_opc = [
            "Tomar preferencialmente após as refeições.",
            "Manter hidratação adequada.",
            "Monitorar pressão arterial diariamente.",
            "Suspender em caso de reação alérgica.",
            "Evitar dirigir ou operar máquinas.",
            "",
        ]
        status_opc = ["ativa", "ativa", "ativa", "suspensa", "encerrada"]

        prescricoes = []

        if not pacientes or not medicamentos:
            return prescricoes

        for _ in range(20):
            paciente = random.choice(pacientes)
            medicamento = random.choice(medicamentos)
            dose = random.choice(descricoes_dose)
            freq = random.choice(frequencias)
            status = random.choice(status_opc)
            obs = random.choice(observacoes_opc)

            prescricao = Prescricao.objects.create(
                paciente=paciente,
                medicamento=medicamento,
                medico=medico_user,
                dose=dose,
                frequencia=freq,
                status=status,
                observacoes=obs,
            )
            prescricoes.append(prescricao)

        return prescricoes

    def _create_administracoes(self, prescricoes, medico_user, enfermeiro_user):
        administracoes = []

        if not prescricoes:
            return administracoes

        usuarios_possiveis = [u for u in [medico_user, enfermeiro_user] if u is not None]

        for _ in range(10):
            prescricao = random.choice(prescricoes)
            usuario = random.choice(usuarios_possiveis)
            # data_hora é auto_now_add, então não precisa setar aqui
            adm = Administracao.objects.create(
                prescricao=prescricao,
                usuario=usuario,
            )
            administracoes.append(adm)

        return administracoes

    def _create_alertas(self, pacientes, prescricoes):
        alertas = []

        if not pacientes:
            return alertas

        agora = timezone.now()

        mensagens_prescricao = [
            "Verificar horário da próxima administração.",
            "Confirmar dose antes da administração.",
            "Avaliar sinais vitais antes da medicação.",
            "Checar histórico de alergias antes da medicação.",
        ]

        mensagens_outros = [
            "Reavaliar dor do paciente.",
            "Monitorar nível de consciência.",
            "Verificar balanço hídrico.",
            "Agendar reavaliação com equipe médica.",
            "Checar glicemia capilar.",
        ]

        # 10 alertas ligados a prescrição (se existirem)
        for i in range(10):
            paciente = random.choice(pacientes)
            prescricao = random.choice(prescricoes) if prescricoes else None
            msg = random.choice(mensagens_prescricao)
            minutos_no_futuro = random.choice([5, 10, 15, 30, 45, 60])
            data_hora = agora + timedelta(minutes=minutos_no_futuro)

            alerta = Alerta.objects.create(
                tipo_alerta="prescricao",
                paciente=paciente,
                prescricao=prescricao,
                mensagem=msg,
                data_hora=data_hora,
                repetir=random.choice([False, False, True]),
                repetir_intervalo=random.choice(
                    [choice for choice, _ in Alerta.INTERVALO_CHOICES]
                ) if random.choice([False, True]) else None,
                ativo=True,
            )
            alertas.append(alerta)

        # 5 alertas do tipo "outro"
        for i in range(5):
            paciente = random.choice(pacientes)
            msg = random.choice(mensagens_outros)
            minutos_no_futuro = random.choice([10, 20, 30, 60, 120])
            data_hora = agora + timedelta(minutes=minutos_no_futuro)

            alerta = Alerta.objects.create(
                tipo_alerta="outro",
                paciente=paciente,
                prescricao=None,
                mensagem=msg,
                data_hora=data_hora,
                repetir=False,
                repetir_intervalo=None,
                ativo=True,
            )
            alertas.append(alerta)

        return alertas
