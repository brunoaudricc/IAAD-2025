# Sistema de Gestão de Consultas Médicas

Sistema web desenvolvido em Python com Dash para gerenciamento completo de clínicas, médicos, pacientes, consultas médicas e lista de espera, com dashboard analítico e visualizações interativas.

## 🚀 Tecnologias

- Python 3.x
- Dash & Dash Bootstrap Components
- MySQL 8.0
- Pandas
- Plotly (visualizações de dados)
- Font Awesome (ícones)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- MySQL Server 8.0
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/brunoaudricc/IAAD-2025.git
cd IAAD-2025
```

2. Crie um ambiente virtual:
- **Windows**
```powershell
python -m venv .venv
```
- **Linux ou macOS**
```bash
python3 -m venv .venv
```

3. Ative o ambiente virtual:
- **Windows**
```powershell
.\.venv\Scripts\Activate
```
- **Linux ou macOS**
```bash
source .venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure as credenciais do banco de dados:
```bash
# Copie o arquivo de exemplo
cp config.example.py config.py
```

Edite o arquivo `config.py` e configure suas credenciais:
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'GestaoClinica',
    'user': 'root',
    'password': 'sua_senha_aqui'  # ALTERAR COM SUA SENHA
}
```

> ⚠️ **Importante**: O arquivo `config.py` está no `.gitignore` e não será commitado. Mantenha suas credenciais seguras!

6. Execute o banco de dados SQL:

**Via MySQL Workbench**
- Abra o MySQL Workbench
- Conecte ao servidor MySQL
- Abra uma nova Query Tab (Ctrl+T)
- Vá em File → Open SQL Script
- Selecione o arquivo `BD Consultas Médicas.sql`
- Clique no ícone de raio ⚡ para executar todo o script


## ▶️ Como Executar

1. Certifique-se de que o MySQL Server está rodando

2. Ative o ambiente virtual (se ainda não estiver ativo):
- **Windows**
```powershell
.\.venv\Scripts\Activate
```
- **Linux ou macOS**
```bash
source .venv/bin/activate
```

3. Execute o aplicativo:
```bash
python app.py
```

4. Abra o navegador e acesse:
```
http://127.0.0.1:8050
```

## 🛑 Para Desativar o Ambiente Virtual

```bash
deactivate
```

## 📌 Funcionalidades

### 🏠 Dashboard Inicial
- **KPIs em tempo real**: Total de clínicas, médicos, pacientes e consultas
- **Design moderno**: Interface responsiva com gradientes e animações
- **Cards interativos**: Visualização clara dos principais indicadores

### 📊 CRUD Completo

#### 🏥 Clínicas
- ✅ Listar todas as clínicas cadastradas
- ✅ Adicionar novas clínicas (código de 7 dígitos)
- ✅ Editar informações das clínicas
- ✅ Excluir clínicas (com validação de integridade referencial)

#### 👨‍⚕️ Médicos
- ✅ Listar médicos com informações completas
- ✅ Adicionar médicos com especialidade e dados de contato
- ✅ Editar cadastro de médicos
- ✅ Excluir médicos (com validação de vínculos)
- ✅ **Filtros avançados**: Nome, especialidade, gênero e ordenação

#### 👥 Pacientes
- ✅ Listar pacientes cadastrados
- ✅ Adicionar novos pacientes (validação de CPF)
- ✅ Editar informações dos pacientes
- ✅ Excluir pacientes (com validação de consultas)
- ✅ **Filtros avançados**: Nome, faixa etária, gênero e mínimo de consultas

#### 📅 Consultas
- ✅ Listar todas as consultas agendadas
- ✅ Agendar novas consultas (seleção de clínica, médico e paciente)
- ✅ Editar horários de consultas
- ✅ Excluir consultas
- ✅ **Filtros avançados**: Paciente, clínica, especialidade e período de datas
- ✅ Validação de chave composta (CodCli + CodMed + CPF + Data_Hora)

#### ⏱️ Lista de Espera
- ✅ Gerenciar fila de espera para consultas
- ✅ Adicionar pacientes à lista de espera com prioridade
- ✅ Visualizar tempo de espera calculado automaticamente
- ✅ Cancelar itens da lista de espera
- ✅ **Filtros avançados**: Especialidade, prioridade, período e ordenação personalizada
- ✅ Status de acompanhamento (Aguardando, Confirmado, Cancelado)

### 📈 Visualizações e Análises (Gráficos)

#### Análises de Consultas
- **Consultas por Especialidade**: Gráfico de pizza mostrando distribuição por área médica
- **Crescimento de Consultas**: Linha temporal dos últimos 6 meses
- **Consultas por Clínica**: Comparação entre unidades
- **Lista de Espera vs Consultas Agendadas**: Comparativo em barras

#### Análises de Profissionais e Pacientes
- **Top 10 Médicos**: Ranking dos médicos com mais consultas
- **Distribuição por Gênero (Médicos)**: Visualização da composição do corpo clínico
- **Distribuição por Gênero (Pacientes)**: Perfil demográfico dos pacientes
- **Faixa Etária dos Pacientes**: Distribuição por grupos de idade

#### Análises Operacionais
- **Pacientes Mais Frequentes**: Top 10 pacientes com mais consultas
- **Taxa de Ocupação por Clínica**: Percentual de utilização
- **Horários de Pico**: Análise dos períodos de maior demanda

## 📝 Operações Disponíveis

### Adicionar
- Cadastro de novos registros com validação de campos obrigatórios
- Feedback visual de sucesso ou erro

### Listar
- Visualização de todos os registros em tabelas interativas
- Atualização automática após operações CRUD
- Filtros avançados para busca personalizada

### Editar
1. Digite a chave primária do registro (Código/CPF)
2. Clique em "Buscar" para carregar os dados
3. Os campos serão preenchidos automaticamente
4. Altere os campos desejados
5. Confirme a atualização

### Excluir
1. Digite a chave primária do registro
2. Clique em "Buscar" para visualizar os dados
3. Revise as informações apresentadas
4. Confirme a exclusão
5. Sistema valida integridade referencial antes de excluir

## 📂 Estrutura do Projeto

```
IAAD-2025/
├── app.py                      # Aplicação principal Dash
├── config.py                   # Configurações do banco (não commitado)
├── config.example.py           # Exemplo de configuração
├── requirements.txt            # Dependências Python
├── BD Consultas Médicas.sql    # Script do banco de dados
├── modelo EER.mwb             # Modelo EER do MySQL Workbench
├── .gitignore                 # Arquivos ignorados pelo Git
└── README.md                  # Este arquivo
```

## 🛠️ Tecnologias e Bibliotecas

- **dash**: Framework web para Python
- **dash-bootstrap-components**: Componentes Bootstrap para Dash
- **mysql-connector-python**: Conector MySQL
- **pandas**: Manipulação e análise de dados
- **plotly**: Visualizações gráficas interativas

## 📄 Licença

Este projeto está sob a licença especificada no arquivo LICENSE.

---

**Desenvolvido para a disciplina de Introdução a Arquitetura e Administração de Dados (IAAD)**
