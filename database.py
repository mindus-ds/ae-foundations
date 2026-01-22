"""
Configuração de conexão com o banco de dados teste commit
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Paciente(db.Model):
    """Modelo para tabela de pacientes"""
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    data_nascimento = db.Column(db.Date)
    endereco = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com consultas
    consultas = db.relationship('Consulta', backref='paciente', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Paciente {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'email': self.email,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d') if self.data_nascimento else None,
            'endereco': self.endereco,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Consulta(db.Model):
    """Modelo para tabela de consultas"""
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    data_consulta = db.Column(db.Date, nullable=False)
    hora_consulta = db.Column(db.Time, nullable=False)
    medico = db.Column(db.String(200), nullable=False)
    especialidade = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='Agendada')  # Agendada, Realizada, Cancelada
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Consulta {self.id} - {self.paciente.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'paciente_nome': self.paciente.nome,
            'data_consulta': self.data_consulta.strftime('%Y-%m-%d'),
            'hora_consulta': self.hora_consulta.strftime('%H:%M'),
            'medico': self.medico,
            'especialidade': self.especialidade,
            'observacoes': self.observacoes,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


def init_db(app):
    """Inicializa o banco de dados"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("✓ Banco de dados inicializado com sucesso!")
