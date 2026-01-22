"""
Script para gerar dados dummy (pacientes e consultas)
Execute: python seed_data.py
"""
from datetime import datetime, timedelta
import random
from faker import Faker
from app import app
from database import db, Paciente, Consulta

# Configuração
fake = Faker('pt_BR')  # Dados em português do Brasil
random.seed(42)  # Para resultados reproduzíveis

# Configurações de quantidade
NUM_PACIENTES = 50
NUM_CONSULTAS = 100

# Especialidades médicas
ESPECIALIDADES = [
    'Cardiologia', 'Dermatologia', 'Ortopedia', 'Pediatria',
    'Ginecologia', 'Oftalmologia', 'Neurologia', 'Psiquiatria',
    'Endocrinologia', 'Urologia', 'Otorrinolaringologia',
    'Gastroenterologia', 'Pneumologia', 'Reumatologia'
]

# Status de consultas
STATUS_CONSULTAS = ['Agendada', 'Realizada', 'Cancelada']


def gerar_cpf():
    """Gera um CPF válido formatado"""
    cpf = [random.randint(0, 9) for _ in range(9)]
    
    # Primeiro dígito verificador
    soma = sum((10 - i) * cpf[i] for i in range(9))
    digito1 = 11 - (soma % 11)
    digito1 = digito1 if digito1 < 10 else 0
    cpf.append(digito1)
    
    # Segundo dígito verificador
    soma = sum((11 - i) * cpf[i] for i in range(10))
    digito2 = 11 - (soma % 11)
    digito2 = digito2 if digito2 < 10 else 0
    cpf.append(digito2)
    
    return f"{cpf[0]}{cpf[1]}{cpf[2]}.{cpf[3]}{cpf[4]}{cpf[5]}.{cpf[6]}{cpf[7]}{cpf[8]}-{cpf[9]}{cpf[10]}"


def gerar_telefone():
    """Gera um telefone celular brasileiro formatado"""
    ddd = random.choice(['11', '21', '31', '41', '51', '61', '71', '81', '91'])
    numero = f"9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    return f"({ddd}) {numero}"


def gerar_pacientes(quantidade):
    """Gera pacientes dummy"""
    print(f"\n📋 Gerando {quantidade} pacientes...")
    pacientes = []
    
    for i in range(quantidade):
        paciente = Paciente(
            nome=fake.name(),
            cpf=gerar_cpf(),
            telefone=gerar_telefone(),
            email=fake.email(),
            data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=90),
            endereco=f"{fake.street_address()}, {fake.city()}/{fake.state_abbr()}"
        )
        pacientes.append(paciente)
        
        if (i + 1) % 10 == 0:
            print(f"  ✓ {i + 1} pacientes gerados...")
    
    print(f"✅ {quantidade} pacientes gerados com sucesso!")
    return pacientes


def gerar_consultas(pacientes, quantidade):
    """Gera consultas dummy para os pacientes"""
    print(f"\n📅 Gerando {quantidade} consultas...")
    consultas = []
    
    # Data base para gerar consultas (passado e futuro)
    data_base = datetime.now()
    
    for i in range(quantidade):
        paciente = random.choice(pacientes)
        especialidade = random.choice(ESPECIALIDADES)
        
        # Gera data entre 6 meses atrás e 3 meses à frente
        dias_offset = random.randint(-180, 90)
        data_consulta = data_base + timedelta(days=dias_offset)
        
        # Hora entre 8h e 18h
        hora = random.randint(8, 17)
        minuto = random.choice([0, 15, 30, 45])
        hora_consulta = datetime.strptime(f"{hora:02d}:{minuto:02d}", '%H:%M').time()
        
        # Nome do médico baseado na especialidade
        nome_medico = f"Dr(a). {fake.name()}"
        
        # Define status baseado na data
        if data_consulta.date() < datetime.now().date():
            status = random.choices(
                ['Realizada', 'Cancelada'],
                weights=[0.85, 0.15]  # 85% realizadas, 15% canceladas
            )[0]
        else:
            status = 'Agendada'
        
        # Observações aleatórias
        observacoes_opcoes = [
            'Consulta de rotina',
            'Retorno de exames',
            'Primeira consulta',
            'Acompanhamento',
            f'Queixa: {random.choice(["dor", "febre", "tosse", "mal-estar"])}',
            'Check-up anual',
            None
        ]
        
        consulta = Consulta(
            paciente_id=paciente.id,
            data_consulta=data_consulta.date(),
            hora_consulta=hora_consulta,
            medico=nome_medico,
            especialidade=especialidade,
            observacoes=random.choice(observacoes_opcoes),
            status=status
        )
        consultas.append(consulta)
        
        if (i + 1) % 20 == 0:
            print(f"  ✓ {i + 1} consultas geradas...")
    
    print(f"✅ {quantidade} consultas geradas com sucesso!")
    return consultas


def limpar_dados():
    """Remove todos os dados existentes"""
    print("\n🗑️  Limpando dados existentes...")
    try:
        Consulta.query.delete()
        Paciente.query.delete()
        db.session.commit()
        print("✅ Dados limpos com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao limpar dados: {e}")
        db.session.rollback()
        return False


def seed_database():
    """Função principal para popular o banco de dados"""
    print("=" * 60)
    print("🌱 SEED DE DADOS - Sistema de Consultas Médicas")
    print("=" * 60)
    
    with app.app_context():
        # Pergunta se quer limpar dados existentes
        resposta = input("\n⚠️  Deseja limpar os dados existentes? (s/n): ").lower()
        if resposta == 's':
            if not limpar_dados():
                return
        
        print(f"\n📊 Configuração:")
        print(f"  • Pacientes: {NUM_PACIENTES}")
        print(f"  • Consultas: {NUM_CONSULTAS}")
        
        try:
            # Gera e salva pacientes
            pacientes = gerar_pacientes(NUM_PACIENTES)
            db.session.add_all(pacientes)
            db.session.commit()
            print(f"💾 {len(pacientes)} pacientes salvos no banco!")
            
            # Gera e salva consultas
            consultas = gerar_consultas(pacientes, NUM_CONSULTAS)
            db.session.add_all(consultas)
            db.session.commit()
            print(f"💾 {len(consultas)} consultas salvas no banco!")
            
            # Estatísticas
            print("\n" + "=" * 60)
            print("📈 ESTATÍSTICAS FINAIS")
            print("=" * 60)
            print(f"Total de pacientes: {Paciente.query.count()}")
            print(f"Total de consultas: {Consulta.query.count()}")
            print(f"  • Agendadas: {Consulta.query.filter_by(status='Agendada').count()}")
            print(f"  • Realizadas: {Consulta.query.filter_by(status='Realizada').count()}")
            print(f"  • Canceladas: {Consulta.query.filter_by(status='Cancelada').count()}")
            print("\n✅ Dados gerados com sucesso!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Erro ao gerar dados: {e}")
            db.session.rollback()


if __name__ == '__main__':
    seed_database()
