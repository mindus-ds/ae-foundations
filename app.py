"""
Sistema de Cadastro de Consultas Médicas
Aplicação Flask para gerenciamento de pacientes e consultas
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import db, init_db, Paciente, Consulta
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui-mude-em-producao')

# Configuração do banco de dados (prioriza DATABASE_URL da AWS, senão usa SQLite local)
database_url = os.getenv('DATABASE_URL', 'sqlite:///consultas_medicas.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Verifica conexão antes de usar
    'pool_recycle': 300,    # Recicla conexões a cada 5 min
}

# Inicializa o banco de dados
init_db(app)


# ========== ROTAS PRINCIPAIS ==========

@app.route('/')
def index():
    """Página inicial com estatísticas"""
    total_pacientes = Paciente.query.count()
    total_consultas = Consulta.query.count()
    consultas_agendadas = Consulta.query.filter_by(status='Agendada').count()
    
    # Últimas consultas
    ultimas_consultas = Consulta.query.order_by(Consulta.created_at.desc()).limit(5).all()
    
    return render_template('index.html', 
                         total_pacientes=total_pacientes,
                         total_consultas=total_consultas,
                         consultas_agendadas=consultas_agendadas,
                         ultimas_consultas=ultimas_consultas)


# ========== ROTAS DE PACIENTES ==========

@app.route('/pacientes')
def pacientes():
    """Lista todos os pacientes"""
    todos_pacientes = Paciente.query.order_by(Paciente.nome).all()
    return render_template('pacientes.html', pacientes=todos_pacientes)


@app.route('/pacientes/novo', methods=['GET', 'POST'])
def novo_paciente():
    """Cadastra novo paciente"""
    if request.method == 'POST':
        try:
            # Converte data de nascimento
            data_nasc = None
            if request.form.get('data_nascimento'):
                data_nasc = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date()
            
            paciente = Paciente(
                nome=request.form['nome'],
                cpf=request.form['cpf'],
                telefone=request.form.get('telefone'),
                email=request.form.get('email'),
                data_nascimento=data_nasc,
                endereco=request.form.get('endereco')
            )
            
            db.session.add(paciente)
            db.session.commit()
            
            flash('Paciente cadastrado com sucesso!', 'success')
            return redirect(url_for('pacientes'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar paciente: {str(e)}', 'error')
    
    return render_template('novo_paciente.html')


@app.route('/pacientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    """Edita um paciente existente"""
    paciente = Paciente.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            paciente.nome = request.form['nome']
            paciente.cpf = request.form['cpf']
            paciente.telefone = request.form.get('telefone')
            paciente.email = request.form.get('email')
            paciente.endereco = request.form.get('endereco')
            
            if request.form.get('data_nascimento'):
                paciente.data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date()
            
            db.session.commit()
            flash('Paciente atualizado com sucesso!', 'success')
            return redirect(url_for('pacientes'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar paciente: {str(e)}', 'error')
    
    return render_template('editar_paciente.html', paciente=paciente)


@app.route('/pacientes/deletar/<int:id>', methods=['POST'])
def deletar_paciente(id):
    """Deleta um paciente"""
    try:
        paciente = Paciente.query.get_or_404(id)
        db.session.delete(paciente)
        db.session.commit()
        flash('Paciente deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar paciente: {str(e)}', 'error')
    
    return redirect(url_for('pacientes'))


# ========== ROTAS DE CONSULTAS ==========

@app.route('/consultas')
def consultas():
    """Lista todas as consultas"""
    todas_consultas = Consulta.query.order_by(Consulta.data_consulta.desc(), Consulta.hora_consulta.desc()).all()
    return render_template('consultas.html', consultas=todas_consultas)


@app.route('/consultas/nova', methods=['GET', 'POST'])
def nova_consulta():
    """Agenda nova consulta"""
    if request.method == 'POST':
        try:
            data_consulta = datetime.strptime(request.form['data_consulta'], '%Y-%m-%d').date()
            hora_consulta = datetime.strptime(request.form['hora_consulta'], '%H:%M').time()
            
            consulta = Consulta(
                paciente_id=request.form['paciente_id'],
                data_consulta=data_consulta,
                hora_consulta=hora_consulta,
                medico=request.form['medico'],
                especialidade=request.form.get('especialidade'),
                observacoes=request.form.get('observacoes'),
                status='Agendada'
            )
            
            db.session.add(consulta)
            db.session.commit()
            
            flash('Consulta agendada com sucesso!', 'success')
            return redirect(url_for('consultas'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao agendar consulta: {str(e)}', 'error')
    
    # Busca pacientes para o formulário
    pacientes = Paciente.query.order_by(Paciente.nome).all()
    return render_template('nova_consulta.html', pacientes=pacientes)


@app.route('/consultas/editar/<int:id>', methods=['GET', 'POST'])
def editar_consulta(id):
    """Edita uma consulta existente"""
    consulta = Consulta.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            consulta.paciente_id = request.form['paciente_id']
            consulta.data_consulta = datetime.strptime(request.form['data_consulta'], '%Y-%m-%d').date()
            consulta.hora_consulta = datetime.strptime(request.form['hora_consulta'], '%H:%M').time()
            consulta.medico = request.form['medico']
            consulta.especialidade = request.form.get('especialidade')
            consulta.observacoes = request.form.get('observacoes')
            consulta.status = request.form.get('status', 'Agendada')
            
            db.session.commit()
            flash('Consulta atualizada com sucesso!', 'success')
            return redirect(url_for('consultas'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar consulta: {str(e)}', 'error')
    
    pacientes = Paciente.query.order_by(Paciente.nome).all()
    return render_template('editar_consulta.html', consulta=consulta, pacientes=pacientes)


@app.route('/consultas/deletar/<int:id>', methods=['POST'])
def deletar_consulta(id):
    """Deleta uma consulta"""
    try:
        consulta = Consulta.query.get_or_404(id)
        db.session.delete(consulta)
        db.session.commit()
        flash('Consulta deletada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar consulta: {str(e)}', 'error')
    
    return redirect(url_for('consultas'))


# ========== ROTA DO DASHBOARD ==========

@app.route('/dashboard')
def dashboard():
    """Página para embed de dashboard (iframe)"""
    return render_template('dashboard.html')


# ========== API JSON (OPCIONAL) ==========

@app.route('/api/pacientes')
def api_pacientes():
    """API JSON para listar pacientes"""
    pacientes = Paciente.query.all()
    return jsonify([p.to_dict() for p in pacientes])


@app.route('/api/consultas')
def api_consultas():
    """API JSON para listar consultas"""
    consultas = Consulta.query.all()
    return jsonify([c.to_dict() for c in consultas])


# ========== EXECUÇÃO ==========

if __name__ == '__main__':
    # Roda em 0.0.0.0 para aceitar conexões externas (útil para EC2)
    # Use debug=False em produção
    app.run(host='0.0.0.0', port=5000, debug=True)
