# Sistema de Cadastro de Consultas Médicas

Sistema web para gerenciamento de pacientes e consultas médicas, desenvolvido em Flask.

## 🏥 Funcionalidades

- ✅ Cadastro e gerenciamento de pacientes
- ✅ Agendamento e controle de consultas médicas
- ✅ Dashboard com estatísticas e visualizações
- ✅ Página para embed de dashboards externos (Power BI, Tableau, etc.)
- ✅ Interface responsiva com Tailwind CSS
- ✅ API REST para integração

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para instalação

1. **Clone ou baixe o projeto**

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**
```bash
python app.py
```

4. **Acesse no navegador**
```
http://localhost:5000
```

Para acessar de outra máquina (como EC2):
```
http://SEU_IP_PUBLICO:5000
```

## 📊 Banco de Dados

### Criação do banco (SQLite - Automático)

O banco de dados SQLite será criado automaticamente ao executar `python app.py` pela primeira vez.

### Usando outro banco (PostgreSQL/MySQL)

Edite o arquivo `app.py` e altere a linha:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consultas_medicas.db'
```

Para PostgreSQL:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:senha@localhost/consultas_medicas'
```

Para MySQL:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:senha@localhost/consultas_medicas'
```

### DDL Manual

Se preferir criar as tabelas manualmente, utilize o arquivo `DDL.sql`:
```bash
sqlite3 consultas_medicas.db < DDL.sql
```

## 📁 Estrutura do Projeto

```
ae-foundations/
│
├── app.py                      # Aplicação Flask principal
├── database.py                 # Configuração do banco de dados
├── requirements.txt            # Dependências Python
├── DDL.sql                     # Script SQL para criação de tabelas
│
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── index.html             # Página inicial
│   ├── pacientes.html         # Lista de pacientes
│   ├── novo_paciente.html     # Cadastro de paciente
│   ├── editar_paciente.html   # Edição de paciente
│   ├── consultas.html         # Lista de consultas
│   ├── nova_consulta.html     # Agendamento de consulta
│   ├── editar_consulta.html   # Edição de consulta
│   └── dashboard.html         # Dashboard e embed
│
└── static/                     # Arquivos estáticos (CSS, JS, imagens)
```

## 🔌 API REST

### Endpoints disponíveis

- `GET /api/pacientes` - Lista todos os pacientes (JSON)
- `GET /api/consultas` - Lista todas as consultas (JSON)

Exemplo de uso:
```bash
curl http://localhost:5000/api/pacientes
```

## 🌐 Deploy em EC2 (AWS)

1. **Configure o Security Group**
   - Libere a porta 5000 (ou 80/443 para produção)

2. **Instale as dependências**
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt
```

3. **Execute a aplicação**
```bash
python3 app.py
```

Para rodar em background:
```bash
nohup python3 app.py &
```

### Produção com Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📈 Dashboard Embed

A página de dashboard permite incorporar dashboards externos via iframe:
- Power BI
- Tableau
- Google Data Studio / Looker Studio
- Metabase
- Apache Superset
- Grafana

Basta inserir a URL de embed na interface.

## 🔐 Segurança

**IMPORTANTE para produção:**
- Altere a `SECRET_KEY` no arquivo `app.py`
- Use variáveis de ambiente para credenciais
- Configure HTTPS
- Use um servidor WSGI (Gunicorn/uWSGI)
- Configure firewall adequadamente

## 📝 Licença

Este projeto é de uso livre para fins educacionais e comerciais.

## 👤 Autor

MindusDS - Sistema de Gestão de Consultas Médicas

## 📞 Suporte

Em caso de dúvidas ou problemas, consulte a documentação do Flask: https://flask.palletsprojects.com/
