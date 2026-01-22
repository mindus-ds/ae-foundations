-- ============================================
-- DDL - Sistema de Cadastro de Consultas Médicas
-- Database: PostgreSQL / MySQL / SQLite compatível
-- ============================================

-- Criar banco de dados (se necessário)
-- Para PostgreSQL/MySQL:
-- CREATE DATABASE consultas_medicas;
-- USE consultas_medicas;

-- ============================================
-- TABELA: pacientes
-- Descrição: Armazena informações dos pacientes
-- ============================================

CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- SQLite
    -- id SERIAL PRIMARY KEY,                 -- PostgreSQL
    -- id INT AUTO_INCREMENT PRIMARY KEY,     -- MySQL
    
    nome VARCHAR(200) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(100),
    data_nascimento DATE,
    endereco VARCHAR(300),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices para otimização de consultas
    CONSTRAINT idx_cpf UNIQUE (cpf)
);

-- Índice adicional para busca por nome
CREATE INDEX idx_pacientes_nome ON pacientes(nome);


-- ============================================
-- TABELA: consultas
-- Descrição: Armazena informações das consultas médicas
-- ============================================

CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- SQLite
    -- id SERIAL PRIMARY KEY,                 -- PostgreSQL
    -- id INT AUTO_INCREMENT PRIMARY KEY,     -- MySQL
    
    paciente_id INTEGER NOT NULL,
    data_consulta DATE NOT NULL,
    hora_consulta TIME NOT NULL,
    medico VARCHAR(200) NOT NULL,
    especialidade VARCHAR(100),
    observacoes TEXT,
    status VARCHAR(20) DEFAULT 'Agendada',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Chave estrangeira
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    
    -- Constraint de status
    CHECK (status IN ('Agendada', 'Realizada', 'Cancelada'))
);

-- Índices para otimização de consultas
CREATE INDEX idx_consultas_paciente ON consultas(paciente_id);
CREATE INDEX idx_consultas_data ON consultas(data_consulta);
CREATE INDEX idx_consultas_status ON consultas(status);


-- ============================================
-- INSERÇÕES DE EXEMPLO (OPCIONAL)
-- ============================================

-- Pacientes de exemplo
INSERT INTO pacientes (nome, cpf, telefone, email, data_nascimento, endereco) VALUES
('João da Silva', '123.456.789-00', '(11) 98765-4321', 'joao.silva@email.com', '1985-03-15', 'Rua das Flores, 123 - São Paulo/SP'),
('Maria Santos', '987.654.321-00', '(11) 91234-5678', 'maria.santos@email.com', '1990-07-22', 'Av. Paulista, 456 - São Paulo/SP'),
('Carlos Oliveira', '456.789.123-00', '(21) 99876-5432', 'carlos.oliveira@email.com', '1978-11-30', 'Rua Rio Branco, 789 - Rio de Janeiro/RJ');

-- Consultas de exemplo
INSERT INTO consultas (paciente_id, data_consulta, hora_consulta, medico, especialidade, observacoes, status) VALUES
(1, '2026-01-25', '09:00', 'Dr. Roberto Carvalho', 'Cardiologia', 'Consulta de rotina - check-up anual', 'Agendada'),
(2, '2026-01-26', '14:30', 'Dra. Ana Paula Lima', 'Dermatologia', 'Avaliação de manchas na pele', 'Agendada'),
(1, '2025-12-20', '10:00', 'Dr. Roberto Carvalho', 'Cardiologia', 'Consulta realizada com sucesso', 'Realizada'),
(3, '2026-01-28', '16:00', 'Dr. Pedro Henrique', 'Ortopedia', 'Dor no joelho direito', 'Agendada');


-- ============================================
-- VIEWS ÚTEIS (OPCIONAL)
-- ============================================

-- View: Próximas consultas agendadas
CREATE VIEW IF NOT EXISTS proximas_consultas AS
SELECT 
    c.id,
    p.nome AS paciente_nome,
    p.cpf AS paciente_cpf,
    c.data_consulta,
    c.hora_consulta,
    c.medico,
    c.especialidade,
    c.status
FROM consultas c
JOIN pacientes p ON c.paciente_id = p.id
WHERE c.status = 'Agendada' 
  AND c.data_consulta >= DATE('now')
ORDER BY c.data_consulta, c.hora_consulta;


-- View: Histórico de consultas por paciente
CREATE VIEW IF NOT EXISTS historico_consultas AS
SELECT 
    p.nome AS paciente_nome,
    p.cpf AS paciente_cpf,
    COUNT(c.id) AS total_consultas,
    SUM(CASE WHEN c.status = 'Realizada' THEN 1 ELSE 0 END) AS consultas_realizadas,
    SUM(CASE WHEN c.status = 'Agendada' THEN 1 ELSE 0 END) AS consultas_agendadas,
    SUM(CASE WHEN c.status = 'Cancelada' THEN 1 ELSE 0 END) AS consultas_canceladas
FROM pacientes p
LEFT JOIN consultas c ON p.id = c.paciente_id
GROUP BY p.id, p.nome, p.cpf;


-- ============================================
-- COMANDOS ÚTEIS PARA VERIFICAÇÃO
-- ============================================

-- Listar todos os pacientes
-- SELECT * FROM pacientes ORDER BY nome;

-- Listar todas as consultas com nome do paciente
-- SELECT c.*, p.nome AS paciente_nome 
-- FROM consultas c 
-- JOIN pacientes p ON c.paciente_id = p.id 
-- ORDER BY c.data_consulta DESC;

-- Contar total de pacientes e consultas
-- SELECT 
--     (SELECT COUNT(*) FROM pacientes) AS total_pacientes,
--     (SELECT COUNT(*) FROM consultas) AS total_consultas,
--     (SELECT COUNT(*) FROM consultas WHERE status = 'Agendada') AS consultas_agendadas;
