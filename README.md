# Sistema de Gestão de Consultas Médicas

Sistema web desenvolvido em Python com Dash para gerenciamento de clínicas, médicos, pacientes e consultas médicas.

## 🚀 Tecnologias

- Python 3.x
- Dash & Dash Bootstrap Components
- MySQL
- Pandas

## 📋 Pré-requisitos

- Python 3.8 ou superior
- MySQL Server 8.0
- Banco de dados `GestaoClinica` criado e populado

## 🔧 Instalação

1. Crie um ambiente virtual:
- Windows
```powershell
python -m venv .venv
```
- Linux ou IOS
```powershell
python3 -m venv .venv
```

2. Ative o ambiente virtual:
- Windows
```powershell
.\.venv\Scripts\Activate
```
- Linux ou IOS
```powershell
source .venv/bin/activate
```

3. Instale as dependências:
```powershell
pip install -r requirements.txt
```

4. Configure a senha do MySQL no arquivo `app.py` (linha 319):
```python
password='sua_senha_aqui'  # ALTERAR COM SUA SENHA
```

5. Execute o banco de dados SQL:

**Via MySQL Workbench**
- Abra o MySQL Workbench
- Conecte ao servidor MySQL
- Abra uma nova Query Tab (Ctrl+T)
- Vá em File → Open SQL Script
- Selecione o arquivo "BD Consultas Médicas.sql"
- Clique no ícone de raio ⚡ para executar


## ▶️ Como Executar

1. Ative o ambiente virtual (se ainda não estiver ativo):
- Windows
```powershell
.\.venv\Scripts\Activate
```
- Linux ou IOS
```powershell
source .venv/bin/activate
```

2. Execute o aplicativo:
- Windows
```powershell
python app.py
```
- Linux ou IOS
```powershell
python3 app.py
```

Abra o app no navegador com a seguinte URL`http://127.0.0.1:8050`

## 🛑 Para Desativar o Ambiente Virtual

```powershell
deactivate
```

## 📌 Funcionalidades

### CRUD Completo para:
- ✅ Clínicas (Create, Read, Update, Delete)
- ✅ Médicos (Create, Read, Update, Delete)
- ✅ Pacientes (Create, Read, Update, Delete)
- ✅ Consultas (Create, Read, Update, Delete)

### Dashboard
- Estatísticas gerais do sistema
- Contadores de registros em tempo real

### Operações Disponíveis
- **Adicionar**: Cadastro de novos registros com validação de campos
- **Listar**: Visualização de todos os registros em tabelas interativas
- **Editar**: 
  - Digite a chave primária do registro (Código/CPF)
  - Clique em "Buscar" para carregar os dados
  - Os campos serão preenchidos automaticamente
  - Altere os campos desejados e confirme a atualização
- **Excluir**: 
  - Digite a chave primária do registro
  - Clique em "Buscar" para visualizar os dados
  - Confirme a exclusão após revisar as informações
  - Sistema valida integridade referencial (não permite excluir se houver vínculos)

## 📝 Observações

- Certifique-se de que o MySQL Server está rodando antes de executar o sistema
- O sistema usa conexão local (localhost)
- Todas as operações são refletidas imediatamente no banco de dados
- Interface responsiva com Bootstrap

### ⚠️ Integridade Referencial com CASCADE
- **Ao excluir Clínica/Médico/Paciente**: Todas as consultas vinculadas são automaticamente excluídas (ON DELETE CASCADE)
- **Ao atualizar chaves primárias**: As referências nas consultas são automaticamente atualizadas (ON UPDATE CASCADE)
- O sistema exibe avisos antes de confirmar exclusões que afetarão consultas vinculadas

### 🔑 Chaves Primárias
- **Clínica**: Código (7 dígitos, ex: 0000001)
- **Médico**: Código numérico (ex: 2819374)
- **Paciente**: CPF (11 dígitos, ex: 34512389765)
- **Consulta**: Chave composta (CodCli + CodMed + CPF + Data_Hora)
