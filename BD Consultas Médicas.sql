DROP DATABASE IF EXISTS GestaoClinica;
CREATE DATABASE GestaoClinica;
USE GestaoClinica;

CREATE TABLE Clinica (
    CodCli CHAR(7) PRIMARY KEY, -- Usando CHAR para manter os zeros à esquerda (ex: 0000001)
    NomeCli VARCHAR(100) NOT NULL,
    Endereco VARCHAR(150),
    Telefone VARCHAR(20),
    Email VARCHAR(100)
);

CREATE TABLE Medico (
    CodMed INT PRIMARY KEY,
    NomeMed VARCHAR(100) NOT NULL,
    Genero CHAR(1),
    Telefone VARCHAR(20),
    Email VARCHAR(100),
    Especialidade VARCHAR(50)
);

CREATE TABLE Paciente (
    CpfPaciente VARCHAR(11) PRIMARY KEY,
    NomePac VARCHAR(100) NOT NULL,
    DataNascimento DATE,
    Genero CHAR(1),
    Telefone VARCHAR(20),
    Email VARCHAR(100)
);

CREATE TABLE Consulta (
    CodCli CHAR(7),
    CodMed INT,
    CpfPaciente VARCHAR(11),
    Data_Hora DATETIME,
    
    -- Chaves Estrangeiras com CASCADE
    CONSTRAINT FK_Consulta_Clinica FOREIGN KEY (CodCli) REFERENCES Clinica(CodCli) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Consulta_Medico FOREIGN KEY (CodMed) REFERENCES Medico(CodMed) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Consulta_Paciente FOREIGN KEY (CpfPaciente) REFERENCES Paciente(CpfPaciente) ON DELETE CASCADE ON UPDATE CASCADE,
    
    -- Chave Primária Composta (evita duplicidade de agendamento exato)
    PRIMARY KEY (CodCli, CodMed, CpfPaciente, Data_Hora),
    
    -- Constraint única: Um médico não pode ter múltiplas consultas no mesmo horário na mesma clínica
    CONSTRAINT UQ_Medico_Horario UNIQUE (CodCli, CodMed, Data_Hora),
    
    -- Constraint única: Um paciente não pode ter múltiplas consultas no mesmo horário
    CONSTRAINT UQ_Paciente_Horario UNIQUE (CpfPaciente, Data_Hora),
    
    -- Validação: Data/Hora da consulta deve ser futura (comentado pois dados de exemplo são passados)
    -- CONSTRAINT CHK_Data_Futura CHECK (Data_Hora >= NOW())
    
    -- Validação: Horário de atendimento entre 6h e 22h
    CONSTRAINT CHK_Horario_Comercial CHECK (HOUR(Data_Hora) BETWEEN 6 AND 22)
);

-- Tabela Clínica
INSERT INTO Clinica (CodCli, NomeCli, Endereco, Telefone, Email) VALUES
('0000001', 'Saúde Plus', 'Av. Rosa e Silva, 406, Graças', '(81) 4002-3633', 'saudeplus@mail.com'),
('0000002', 'Visão Recife', 'Av. Governador Agamenon Magalhães, 810', '(81) 3042-1112', 'visaorecife@mail.com');

-- Tabela Médico
INSERT INTO Medico (CodMed, NomeMed, Genero, Telefone, Email, Especialidade) VALUES
(2819374, 'Marcela Gomes', 'F', '(81) 98273-3245', 'marcelagomes@mail.com', 'Pediatria'),
(5793149, 'Amanda Vieira', 'F', '(81) 99240-2571', 'amandavieira@mail.com', 'Pediatria'), -- Mantido email conforme imagem
(8532974, 'Lucas Carvalho', 'M', '(81) 98256-5703', 'lucascarvalho@mail.com', 'Oftalmologia'),
(9183424, 'Alexandre Alencar', 'M', '(81) 99482-4758', 'alexandrealencar@mail.com', 'Oftalmologia');

-- Tabela Paciente
INSERT INTO Paciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email) VALUES
('34512389765', 'Rebeca Lins', '1993-04-15', 'F', '(81) 99945-4177', 'rebeca@mail.com'),
('58961234752', 'Paulo Martins', '2020-08-21', 'M', '(81) 99873-4312', 'paulo@mail.com');

-- Tabela Consulta
INSERT INTO Consulta (CodCli, CodMed, CpfPaciente, Data_Hora) VALUES
('0000001', 2819374, '58961234752', '2025-11-03 15:00:00'),
('0000002', 8532974, '34512389765', '2025-12-10 16:40:00'),
('0000002', 9183424, '34512389765', '2026-01-05 10:30:00');


-- Mais Clínicas
INSERT INTO Clinica (CodCli, NomeCli, Endereco, Telefone, Email) VALUES
('0000003', 'Cardio Vida', 'Rua da Aurora, 295, Boa Vista', '(81) 3222-1010', 'contato@cardiovida.com'),
('0000004', 'Derma Clin', 'Av. Conselheiro Aguiar, 1500, Boa Viagem', '(81) 3465-2020', 'agendamento@dermaclin.com');
-- Mais Clínicas
INSERT INTO Clinica (CodCli, NomeCli, Endereco, Telefone, Email) VALUES
('0000005', 'OrtoMed Recife', 'Rua Benfica, 150, Madalena', '(81) 3227-3030', 'contato@ortomed.com'),
('0000006', 'NeuroCentro', 'Av. Boa Viagem, 3200, Boa Viagem', '(81) 3326-4040', 'agendamento@neurocentro.com'),
('0000007', 'Clínica da Família', 'Rua Imperial, 890, São José', '(81) 3423-5050', 'familia@clinica.com');


-- Mais Médicos
INSERT INTO Medico (CodMed, NomeMed, Genero, Telefone, Email, Especialidade) VALUES
(1122334, 'Roberto Silva', 'M', '(81) 98888-1111', 'robertosilva@mail.com', 'Cardiologia'),
(5566778, 'Carla Dias', 'F', '(81) 97777-2222', 'carladias@mail.com', 'Dermatologia'),
(9988776, 'Fernanda Costa', 'F', '(81) 99999-3333', 'fernandacosta@mail.com', 'Clínico Geral'),
(2233445, 'Patricia Mendes', 'F', '(81) 96666-7777', 'patriciamendes@mail.com', 'Ortopedia'),
(3344556, 'Carlos Eduardo', 'M', '(81) 95555-8888', 'carloseduardo@mail.com', 'Neurologia'),
(4455667, 'Juliana Farias', 'F', '(81) 94444-9999', 'julianafarias@mail.com', 'Pediatria'),
(5566889, 'Ricardo Moura', 'M', '(81) 93333-0000', 'ricardomoura@mail.com', 'Cardiologia'),
(6677990, 'Beatriz Souza', 'F', '(81) 92222-1111', 'beatrizsouza@mail.com', 'Dermatologia'),
(7788001, 'André Lima', 'M', '(81) 91111-2222', 'andrelima@mail.com', 'Ortopedia'),
(8899112, 'Camila Rocha', 'F', '(81) 90000-3333', 'camilarocha@mail.com', 'Clínico Geral'),
(9900223, 'Thiago Barros', 'M', '(81) 98888-4444', 'thiagobarros@mail.com', 'Oftalmologia'),
(1010101, 'Helena Nunes', 'F', '(81) 94400-1212', 'helenanunes@mail.com', 'Ginecologia');

-- Mais Pacientes
INSERT INTO Paciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email) VALUES
('11122233344', 'João Souza', '1985-02-10', 'M', '(81) 91234-5678', 'joaosouza@mail.com'),
('55566677788', 'Maria Oliveira', '1990-11-25', 'F', '(81) 98765-4321', 'mariaoliveira@mail.com'),
('99988877766', 'Pedro Santos', '1975-06-30', 'M', '(81) 95555-4444', 'pedrosantos@mail.com'),
('12345678901', 'Ana Carolina', '1988-03-12', 'F', '(81) 99111-2233', 'anacarolina@mail.com'),
('23456789012', 'Bruno Henrique', '1992-07-18', 'M', '(81) 98222-3344', 'brunohenrique@mail.com'),
('34567890123', 'Claudia Ferreira', '2015-09-05', 'F', '(81) 97333-4455', 'claudiaferreira@mail.com'),
('45678901234', 'Daniel Costa', '1978-12-22', 'M', '(81) 96444-5566', 'danielcosta@mail.com'),
('56789012345', 'Eliana Rodrigues', '1995-05-30', 'F', '(81) 95555-6677', 'elianarodrigues@mail.com'),
('67890123456', 'Fernando Alves', '2018-01-14', 'M', '(81) 94666-7788', 'fernandoalves@mail.com'),
('78901234567', 'Gabriela Santos', '1982-11-08', 'F', '(81) 93777-8899', 'gabrielasantos@mail.com'),
('89012345678', 'Henrique Dias', '1970-04-25', 'M', '(81) 92888-9900', 'henriquedias@mail.com'),
('90123456789', 'Isabela Lima', '2012-06-17', 'F', '(81) 91999-0011', 'isabelalima@mail.com'),
('01234567890', 'Jorge Oliveira', '1965-08-03', 'M', '(81) 90000-1122', 'jorgeoliveira@mail.com'),
('33344455566', 'Laura Mendes', '1994-09-20', 'F', '(81) 94555-3344', 'lauramendes@mail.com');


-- Mais Consultas (Cruzando os dados novos e antigos)
-- Consultas 2025
INSERT INTO Consulta (CodCli, CodMed, CpfPaciente, Data_Hora) VALUES
('0000001', 5793149, '58961234752', '2025-11-04 09:00:00'),
('0000003', 1122334, '11122233344', '2025-11-15 14:00:00'),
('0000004', 5566778, '34512389765', '2025-12-01 11:30:00'),
('0000001', 9988776, '99988877766', '2026-02-20 08:00:00'),
('0000002', 8532974, '55566677788', '2026-03-10 16:00:00'),
('0000005', 2233445, '12345678901', '2025-12-05 10:00:00'),
('0000006', 3344556, '23456789012', '2025-12-08 15:30:00'),
('0000001', 4455667, '34567890123', '2025-12-12 09:00:00'),
('0000003', 5566889, '45678901234', '2025-12-15 14:00:00'),
('0000004', 6677990, '56789012345', '2025-12-18 11:00:00'),
('0000005', 7788001, '67890123456', '2025-12-20 16:00:00'),
('0000007', 8899112, '78901234567', '2025-12-22 08:30:00'),
('0000002', 9900223, '89012345678', '2025-12-27 13:00:00'),
-- Consultas 2026
('0000001', 2819374, '90123456789', '2026-01-03 10:30:00'),
('0000007', 1010101, '33344455566', '2026-01-06 09:00:00'),
('0000006', 3344556, '01234567890', '2026-01-08 14:30:00'),
('0000003', 1122334, '12345678901', '2026-01-10 09:00:00'),
('0000004', 5566778, '23456789012', '2026-01-15 15:00:00'),
('0000005', 2233445, '34512389765', '2026-01-18 11:30:00'),
('0000007', 9988776, '45678901234', '2026-01-22 08:00:00'),
('0000001', 5793149, '67890123456', '2026-01-25 16:30:00'),
('0000002', 8532974, '78901234567', '2026-02-01 10:00:00'),
('0000006', 3344556, '11122233344', '2026-02-05 13:30:00'),
('0000003', 5566889, '56789012345', '2026-02-12 09:30:00'),
('0000004', 6677990, '89012345678', '2026-02-15 14:00:00'),
('0000007', 8899112, '90123456789', '2026-02-18 11:00:00'),
('0000007', 1010101, '33344455566', '2026-07-06 09:00:00');

-- ==================== LISTA DE ESPERA ====================
-- Tabela para armazenar pacientes na lista de espera
CREATE TABLE ListaEspera (
    IdEspera INT AUTO_INCREMENT PRIMARY KEY,
    CodCli CHAR(7) NOT NULL,
    CodMed INT NOT NULL,
    CpfPaciente VARCHAR(11) NOT NULL,
    DataHoraDesejada DATETIME NOT NULL,
    DataHoraCadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    Prioridade INT DEFAULT 0, -- Maior número = maior prioridade (0-5)
    Status ENUM('aguardando', 'agendado', 'expirado', 'cancelado') DEFAULT 'aguardando',
    
    CONSTRAINT FK_Espera_Clinica FOREIGN KEY (CodCli) REFERENCES Clinica(CodCli) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Espera_Medico FOREIGN KEY (CodMed) REFERENCES Medico(CodMed) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Espera_Paciente FOREIGN KEY (CpfPaciente) REFERENCES Paciente(CpfPaciente) ON DELETE CASCADE ON UPDATE CASCADE,
    
    -- Evita que o mesmo paciente esteja 2x na fila para o mesmo médico/clínica/horário aguardando
    CONSTRAINT UQ_Espera_Paciente UNIQUE (CodCli, CodMed, CpfPaciente, DataHoraDesejada, Status),
    
    -- Validação: Prioridade entre 0 e 5
    CONSTRAINT CHK_Prioridade CHECK (Prioridade BETWEEN 0 AND 5),
    
    -- Validação: Horário desejado entre 6h e 22h
    CONSTRAINT CHK_Horario_Desejado CHECK (HOUR(DataHoraDesejada) BETWEEN 6 AND 22)
);

-- Tabela de log para registrar as promoções da lista de espera
CREATE TABLE LogListaEspera (
    IdLog INT AUTO_INCREMENT PRIMARY KEY,
    IdEspera INT,
    CodCli CHAR(7),
    CodMed INT,
    CpfPaciente VARCHAR(11),
    DataHoraConsulta DATETIME,
    DataHoraPromocao DATETIME DEFAULT CURRENT_TIMESTAMP,
    Mensagem VARCHAR(255)
);

-- ==================== PROCEDIMENTO ARMAZENADO ====================
-- Procedimento para promover paciente da lista de espera após cancelamento
-- Deve ser chamado pela aplicação após deletar uma consulta

DELIMITER //

CREATE PROCEDURE sp_promover_lista_espera(
    IN p_cod_cli CHAR(7),
    IN p_cod_med INT,
    IN p_data_hora DATETIME,
    IN p_cpf_cancelado VARCHAR(11)
)
BEGIN
    DECLARE v_id_espera INT;
    DECLARE v_cpf_paciente VARCHAR(11);
    DECLARE v_data_hora_desejada DATETIME;
    
    -- Busca o próximo paciente na lista de espera para o mesmo médico e clínica
    -- Prioriza quem quer horário igual ou anterior (já passou da hora desejada)
    -- Ordena por: 1) Prioridade maior, 2) Data desejada mais próxima, 3) Cadastro mais antigo
    SELECT IdEspera, CpfPaciente, DataHoraDesejada
    INTO v_id_espera, v_cpf_paciente, v_data_hora_desejada
    FROM ListaEspera
    WHERE CodCli = p_cod_cli
      AND CodMed = p_cod_med
      AND Status = 'aguardando'
      -- Busca quem quer este horário OU horários anteriores (já passou do desejado)
      AND DataHoraDesejada <= p_data_hora
      -- Garante que o paciente não tem conflito de horário
      AND CpfPaciente NOT IN (
          SELECT CpfPaciente FROM Consulta 
          WHERE Data_Hora = p_data_hora
      )
    ORDER BY 
        Prioridade DESC,                                    -- Maior prioridade primeiro
        ABS(TIMESTAMPDIFF(MINUTE, DataHoraDesejada, p_data_hora)) ASC,  -- Horário mais próximo
        DataHoraCadastro ASC                               -- Mais antigo na fila
    LIMIT 1;
    
    -- Se encontrou alguém na lista de espera
    IF v_id_espera IS NOT NULL THEN
        -- Insere a nova consulta para o paciente da lista de espera
        INSERT INTO Consulta (CodCli, CodMed, CpfPaciente, Data_Hora)
        VALUES (p_cod_cli, p_cod_med, v_cpf_paciente, p_data_hora);
        
        -- Atualiza o status na lista de espera
        UPDATE ListaEspera
        SET Status = 'agendado'
        WHERE IdEspera = v_id_espera;
        
        -- Registra no log
        INSERT INTO LogListaEspera (IdEspera, CodCli, CodMed, CpfPaciente, DataHoraConsulta, Mensagem)
        VALUES (v_id_espera, p_cod_cli, p_cod_med, v_cpf_paciente, p_data_hora, 
                CONCAT('Paciente promovido da lista de espera. Consulta original cancelada por: ', p_cpf_cancelado, 
                       '. Horário desejado original: ', v_data_hora_desejada));
    END IF;
END //

DELIMITER ;

-- ==================== INSERIR DADOS NA LISTA DE ESPERA (EXEMPLO) ====================
-- Pacientes aguardando vaga para consultas existentes
INSERT INTO ListaEspera (CodCli, CodMed, CpfPaciente, DataHoraDesejada, Prioridade) VALUES
-- Esperando vaga na consulta do dia 2025-12-10 16:40:00 com Dr. Lucas Carvalho na Visão Recife
('0000002', 8532974, '11122233344', '2025-12-10 16:40:00', 1),
('0000002', 8532974, '55566677788', '2025-12-10 16:40:00', 0),

-- Esperando vaga na consulta do dia 2025-12-01 11:30:00 com Dra. Carla Dias na Derma Clin
('0000004', 5566778, '99988877766', '2025-12-01 11:30:00', 2),
('0000004', 5566778, '12345678901', '2025-12-01 11:30:00', 1),

-- Esperando vaga na consulta do dia 2026-01-05 10:30:00 com Dr. Alexandre Alencar na Visão Recife
('0000002', 9183424, '23456789012', '2026-01-05 10:30:00', 0);

SELECT * FROM Consulta;

-- ==================== VISUALIZAR LISTA DE ESPERA ====================
SELECT 
    le.IdEspera,
    c.NomeCli AS Clinica,
    m.NomeMed AS Medico,
    m.Especialidade,
    p.NomePac AS Paciente,
    le.DataHoraDesejada AS 'Data/Hora Desejada',
    le.Prioridade,
    le.Status,
    le.DataHoraCadastro AS 'Data Cadastro'
FROM ListaEspera le
JOIN Clinica c ON le.CodCli = c.CodCli
JOIN Medico m ON le.CodMed = m.CodMed
JOIN Paciente p ON le.CpfPaciente = p.CpfPaciente
ORDER BY le.DataHoraDesejada, le.Prioridade DESC, le.DataHoraCadastro;