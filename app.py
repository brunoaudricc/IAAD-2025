import dash
from dash import dcc, html, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
from config import DB_CONFIG

# Inicializar app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Sistema de Gestão Clínica"

# CSS customizado para design moderno
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <style>
            body {
                background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #e0f2fe 100%) !important;
                background-attachment: fixed;
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            .container-fluid {
                background: transparent !important;
            }
            /* Header com animação */
            h1 {
                color: #0c4a6e !important;
                font-weight: 700;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                animation: fadeInDown 0.6s ease-out;
            }
            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            /* Barra de navegação moderna */
            .nav-pills {
                background: white;
                border-radius: 20px;
                padding: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
                position: relative;
                z-index: 100;
            }
            .nav-pills .nav-link {
                color: #64748b !important;
                background: transparent !important;
                border: none !important;
                font-weight: 600;
                border-radius: 12px;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                margin: 0 4px;
                padding: 12px 20px;
                position: relative;
                overflow: hidden;
                font-size: 0.95rem;
                letter-spacing: 0.3px;
            }
            .nav-pills .nav-link:hover {
                color: #0ea5e9 !important;
                background: rgba(14, 165, 233, 0.04) !important;
                transform: translateY(-2px);
            }
            .nav-pills .nav-link::before {
                content: '';
                position: absolute;
                bottom: 0;
                left: 50%;
                width: 0;
                height: 3px;
                background: linear-gradient(90deg, #0ea5e9 0%, #06b6d4 100%);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                transform: translateX(-50%);
                border-radius: 4px;
            }
            .nav-pills .nav-link.active {
                color: #0ea5e9 !important;
                background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%) !important;
                box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2);
            }
            .nav-pills .nav-link.active::before {
                width: 80%;
            }
            /* Cards KPI com design sofisticado */
            .kpi-card {
                background: white !important;
                border: none !important;
                border-radius: 20px !important;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08) !important;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
                overflow: hidden;
                position: relative;
            }
            .kpi-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 5px;
                background: linear-gradient(90deg, var(--card-color-1) 0%, var(--card-color-2) 100%);
            }
            .kpi-card:nth-child(1) {
                --card-color-1: #0ea5e9;
                --card-color-2: #06b6d4;
            }
            .kpi-card:nth-child(2) {
                --card-color-1: #10b981;
                --card-color-2: #059669;
            }
            .kpi-card:nth-child(3) {
                --card-color-1: #3b82f6;
                --card-color-2: #2563eb;
            }
            .kpi-card:nth-child(4) {
                --card-color-1: #8b5cf6;
                --card-color-2: #7c3aed;
            }
            .kpi-card:hover {
                transform: translateY(-8px) scale(1.02) !important;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15) !important;
            }
            .kpi-card .card-body {
                padding: 2rem !important;
                position: relative;
                min-height: 150px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            .kpi-icon {
                font-size: 3.5rem;
                opacity: 0.1;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                transition: all 0.4s ease;
                z-index: 0;
            }
            .kpi-card:hover .kpi-icon {
                opacity: 0.2;
                transform: translate(-50%, -50%) scale(1.15);
            }
            .kpi-label {
                font-size: 0.85rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: #64748b;
                margin-bottom: 0.75rem;
                z-index: 1;
                position: relative;
            }
            .kpi-value {
                font-size: 2.8rem;
                font-weight: 700;
                line-height: 1;
                background: linear-gradient(135deg, var(--card-color-1) 0%, var(--card-color-2) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                z-index: 1;
                position: relative;
            }
            /* Cards normais */
            .card {
                border: none !important;
                border-radius: 15px !important;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
                transition: all 0.3s ease !important;
                background: white !important;
            }
            .card:hover {
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12) !important;
            }
            /* Section headers */
            h2, h3, h4 {
                color: #0c4a6e !important;
                font-weight: 700;
            }
            /* Labels */
            label {
                color: #1e40af !important;
                font-weight: 600 !important;
                margin-bottom: 8px !important;
                font-size: 0.9rem;
            }
            /* Botões */
            .btn {
                border-radius: 10px !important;
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
                padding: 10px 24px !important;
                border: none !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
            }
            .btn:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15) !important;
            }
            .btn-primary {
                background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%) !important;
            }
            .btn-success {
                background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            }
            .btn-warning {
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
            }
            .btn-danger {
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
            }
            .btn-info {
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            }
            /* Inputs */
            .form-control, .form-select {
                border-radius: 10px !important;
                border: 2px solid #e0f2fe !important;
                transition: all 0.3s ease !important;
                padding: 10px 16px !important;
            }
            .form-control:focus, .form-select:focus {
                border-color: #0ea5e9 !important;
                box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1) !important;
            }
            /* Tabelas */
            .dash-table-container {
                border-radius: 15px !important;
                overflow: hidden !important;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
            }
            .dash-spreadsheet-container {
                border-radius: 15px !important;
            }
            /* Alerts */
            .alert {
                border-radius: 12px !important;
                border: none !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
            }
            /* Dividers */
            hr {
                border: none;
                height: 2px;
                background: linear-gradient(90deg, transparent 0%, #0ea5e9 50%, transparent 100%);
                margin: 2rem 0;
                opacity: 0.3;
            }
            /* Tabs internas (Listar, Adicionar, Editar, Excluir) */
            .nav-tabs {
                border-bottom: 2px solid #e0f2fe !important;
                margin-bottom: 2rem !important;
            }
            .nav-tabs .nav-link {
                color: #64748b !important;
                background: transparent !important;
                border: none !important;
                border-bottom: 3px solid transparent !important;
                font-weight: 600 !important;
                padding: 12px 24px !important;
                transition: all 0.3s ease !important;
                position: relative;
                margin-bottom: -2px !important;f
            }
            .nav-tabs .nav-link:hover {
                color: #0ea5e9 !important;
                background: rgba(14, 165, 233, 0.05) !important;
                border-radius: 8px 8px 0 0 !important;
            }
            .nav-tabs .nav-link.active {
                color: #0ea5e9 !important;
                background: white !important;
                border-bottom: 3px solid #0ea5e9 !important;
                border-radius: 8px 8px 0 0 !important;
                box-shadow: 0 -2px 8px rgba(14, 165, 233, 0.1) !important;
            }
            .nav-tabs .nav-link i {
                margin-right: 8px;
                font-size: 1.1rem;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Função de conexão com o banco de dados
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Função para executar queries SELECT
def execute_query(query, params=None):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        except Error as e:
            print(f"Erro na consulta: {e}")
            return []
    return []

# Função para executar queries INSERT, UPDATE, DELETE
def execute_update(query, params=None):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Erro na operação: {e}")
            return False
    return False



# Layout do app
app.layout = dbc.Container([
    # Header elegante
    dbc.Row([
        dbc.Col([
            html.Div([
                html.I(className="fas fa-heartbeat", style={
                    'fontSize': '3rem',
                    'color': '#0ea5e9',
                    'marginBottom': '1rem'
                }),
                html.H1("Sistema de Gestão de Consultas Médicas", className="text-center mb-2"),
                html.P("Gestão completa de clínicas, médicos, pacientes e consultas", 
                       className="text-center text-muted mb-0",
                       style={'fontSize': '1.1rem'})
            ], className="text-center py-4")
        ], width=12)
    ], justify="center"),
    
    html.Hr(),
    
    # Navegação moderna em pills - centralizada
    dbc.Row([
        dbc.Col([
            dbc.Nav([
                dbc.NavLink([html.I(className="fas fa-home me-2"), "Home"], href="#", id="tab-home", active=True),
                dbc.NavLink([html.I(className="fas fa-hospital me-2"), "Clínicas"], href="#", id="tab-clinicas"),
                dbc.NavLink([html.I(className="fas fa-user-md me-2"), "Médicos"], href="#", id="tab-medicos"),
                dbc.NavLink([html.I(className="fas fa-users me-2"), "Pacientes"], href="#", id="tab-pacientes"),
                dbc.NavLink([html.I(className="fas fa-calendar-check me-2"), "Consultas"], href="#", id="tab-consultas"),
            ], pills=True, className="mb-4", justified=True)
        ], lg=10, md=12)
    ], justify="center"),
    
    # Conteúdo centralizado
    dbc.Row([
        dbc.Col([
            html.Div(id="tab-content", className="p-3")
        ], lg=11, md=12)
    ], justify="center"),
    
    dcc.Store(id='refresh-trigger', data=0),
    dcc.Store(id='active-tab', data='home')
], fluid=True, className="px-4")

# Callback para controlar navegação
@app.callback(
    [Output('active-tab', 'data'),
     Output('tab-home', 'active'),
     Output('tab-clinicas', 'active'),
     Output('tab-medicos', 'active'),
     Output('tab-pacientes', 'active'),
     Output('tab-consultas', 'active')],
    [Input('tab-home', 'n_clicks'),
     Input('tab-clinicas', 'n_clicks'),
     Input('tab-medicos', 'n_clicks'),
     Input('tab-pacientes', 'n_clicks'),
     Input('tab-consultas', 'n_clicks')],
    prevent_initial_call=False
)
def update_active_tab(home_clicks, clinicas_clicks, medicos_clicks, pacientes_clicks, consultas_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return 'home', True, False, False, False, False
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    tabs = {
        'tab-home': ('home', [True, False, False, False, False]),
        'tab-clinicas': ('clinicas', [False, True, False, False, False]),
        'tab-medicos': ('medicos', [False, False, True, False, False]),
        'tab-pacientes': ('pacientes', [False, False, False, True, False]),
        'tab-consultas': ('consultas', [False, False, False, False, True])
    }
    
    if button_id in tabs:
        tab_name, active_states = tabs[button_id]
        return tab_name, *active_states
    
    return 'home', True, False, False, False, False

# Callback para renderizar conteúdo das abas
@app.callback(
    Output("tab-content", "children"),
    [Input("active-tab", "data"),
     Input("refresh-trigger", "data")]
)
def render_tab_content(active_tab, refresh):
    if active_tab == "home":
        return render_home()
    elif active_tab == "clinicas":
        return render_clinicas()
    elif active_tab == "medicos":
        return render_medicos()
    elif active_tab == "pacientes":
        return render_pacientes()
    elif active_tab == "consultas":
        return render_consultas()
    return html.Div("Selecione uma aba")

# ==================== HOME ====================
def render_home():
    # Contar registros
    clinicas = execute_query("SELECT COUNT(*) as total FROM Clinica")
    medicos = execute_query("SELECT COUNT(*) as total FROM Medico")
    pacientes = execute_query("SELECT COUNT(*) as total FROM Paciente")
    consultas = execute_query("SELECT COUNT(*) as total FROM Consulta")
    
    total_clinicas = clinicas[0]['total'] if clinicas else 0
    total_medicos = medicos[0]['total'] if medicos else 0
    total_pacientes = pacientes[0]['total'] if pacientes else 0
    total_consultas = consultas[0]['total'] if consultas else 0
    
    return html.Div([
        # Título centralizado
        dbc.Row([
            dbc.Col([
                html.H2([
                    html.I(className="fas fa-chart-line me-3", style={'color': '#0ea5e9'}),
                    "Dashboard"
                ], className="text-center mb-4")
            ], width=12)
        ]),
        
        # Cards KPI centralizados
        dbc.Row([
            # Card Clínicas
            dbc.Col([
                html.Div([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="fas fa-hospital kpi-icon", style={'color': '#0ea5e9'}),
                            html.Div([
                                html.Div("Total de Clínicas", className="kpi-label text-center"),
                                html.Div(f"{total_clinicas:,}", className="kpi-value text-center")
                            ])
                        ], style={'textAlign': 'center', 'position': 'relative'})
                    ], className="kpi-card")
                ])
            ], lg=3, md=6, sm=12, className="mb-4"),
            
            # Card Médicos
            dbc.Col([
                html.Div([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="fas fa-user-md kpi-icon", style={'color': '#10b981'}),
                            html.Div([
                                html.Div("Total de Médicos", className="kpi-label text-center"),
                                html.Div(f"{total_medicos:,}", className="kpi-value text-center")
                            ])
                        ], style={'textAlign': 'center', 'position': 'relative'})
                    ], className="kpi-card")
                ])
            ], lg=3, md=6, sm=12, className="mb-4"),
            
            # Card Pacientes
            dbc.Col([
                html.Div([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="fas fa-users kpi-icon", style={'color': '#3b82f6'}),
                            html.Div([
                                html.Div("Total de Pacientes", className="kpi-label text-center"),
                                html.Div(f"{total_pacientes:,}", className="kpi-value text-center")
                            ])
                        ], style={'textAlign': 'center', 'position': 'relative'})
                    ], className="kpi-card")
                ])
            ], lg=3, md=6, sm=12, className="mb-4"),
            
            # Card Consultas
            dbc.Col([
                html.Div([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="fas fa-calendar-check kpi-icon", style={'color': '#8b5cf6'}),
                            html.Div([
                                html.Div("Total de Consultas", className="kpi-label text-center"),
                                html.Div(f"{total_consultas:,}", className="kpi-value text-center")
                            ])
                        ], style={'textAlign': 'center', 'position': 'relative'})
                    ], className="kpi-card")
                ])
            ], lg=3, md=6, sm=12, className="mb-4"),
        ], justify="center"),
        
        # Card informativo centralizado
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5([
                            html.I(className="fas fa-info-circle me-2", style={'color': '#0ea5e9'}),
                            "Bem-vindo ao Sistema"
                        ], className="mb-3 text-center"),
                        html.P([
                            "Utilize a navegação acima para acessar as diferentes seções do sistema. ",
                            "Você pode gerenciar clínicas, cadastrar médicos, registrar pacientes e agendar consultas."
                        ], className="text-muted mb-0 text-center")
                    ])
                ], style={
                    'background': 'linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%)',
                    'border': '2px solid #e0f2fe'
                })
            ], lg=10, md=12)
        ], justify="center")
    ])

# ==================== CLÍNICAS ====================
def render_clinicas():
    clinicas = execute_query("SELECT * FROM Clinica")
    df = pd.DataFrame(clinicas) if clinicas else pd.DataFrame()
    
    return html.Div([
        html.H3("Gestão de Clínicas", className="mb-4"),
        dbc.Tabs(active_tab="tab-listar-clinicas", children=[
            dbc.Tab(label="Listar", tab_id="tab-listar-clinicas", children=[
                html.Div([
                    dash_table.DataTable(
                        id='table-clinicas',
                        columns=[{"name": i, "id": i} for i in df.columns] if not df.empty else [],
                        data=df.to_dict('records') if not df.empty else [],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                    )
                ], className="mt-3")
            ]),
            dbc.Tab(label="Adicionar", tab_id="tab-adicionar-clinicas", children=[
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Código (7 dígitos)"),
                            dbc.Input(id="clinica-cod", type="text", maxLength=7)
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Nome da Clínica"),
                            dbc.Input(id="clinica-nome", type="text")
                        ], width=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Endereço"),
                            dbc.Input(id="clinica-endereco", type="text")
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Telefone"),
                            dbc.Input(id="clinica-telefone", type="text")
                        ], width=6),
                    ], className="mt-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Email"),
                            dbc.Input(id="clinica-email", type="email")
                        ], width=6),
                    ], className="mt-3"),
                    dbc.Button("Cadastrar Clínica", id="btn-add-clinica", color="primary", className="mt-3"),
                    html.Div(id="msg-clinica", className="mt-3")
                ], className="mt-3")
            ]),
            dbc.Tab(label="Editar", tab_id="tab-editar-clinicas", children=[
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Código da Clínica (7 dígitos)"),
                            dbc.Input(id="clinica-edit-cod", type="text", maxLength=7, placeholder="Digite o código")
                        ], width=6),
                        dbc.Col([
                            dbc.Button("Buscar", id="btn-search-clinica", color="info", className="mt-4")
                        ], width=2),
                    ]),
                    html.Hr(className="mt-3"),
                    html.Div(id="clinica-edit-form", children=[
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Nome da Clínica"),
                                dbc.Input(id="clinica-edit-nome", type="text", disabled=True)
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Endereço"),
                                dbc.Input(id="clinica-edit-endereco", type="text", disabled=True)
                            ], width=6),
                        ], className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Telefone"),
                                dbc.Input(id="clinica-edit-telefone", type="text", disabled=True)
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Email"),
                                dbc.Input(id="clinica-edit-email", type="email", disabled=True)
                            ], width=6),
                        ], className="mt-3"),
                        dbc.Button("Atualizar Clínica", id="btn-update-clinica", color="warning", className="mt-3", disabled=True),
                    ]),
                    html.Div(id="msg-edit-clinica", className="mt-3")
                ], className="mt-3")
            ]),
            dbc.Tab(label="Excluir", tab_id="tab-excluir-clinicas", children=[
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Código da Clínica (7 dígitos)"),
                            dbc.Input(id="clinica-delete-cod", type="text", maxLength=7, placeholder="Digite o código")
                        ], width=6),
                        dbc.Col([
                            dbc.Button("Buscar", id="btn-search-delete-clinica", color="info", className="mt-4")
                        ], width=2),
                    ]),
                    html.Hr(className="mt-3"),
                    html.Div(id="clinica-delete-info", children=[
                        dbc.Alert("Digite um código e clique em Buscar para visualizar os dados.", color="info")
                    ]),
                    dbc.Button("Confirmar Exclusão", id="btn-delete-clinica", color="danger", className="mt-3", disabled=True),
                    html.Div(id="msg-delete-clinica", className="mt-3")
                ], className="mt-3")
            ]),
        ])
    ])

@app.callback(
    [Output("msg-clinica", "children"),
     Output("refresh-trigger", "data")],
    Input("btn-add-clinica", "n_clicks"),
    [State("clinica-cod", "value"),
     State("clinica-nome", "value"),
     State("clinica-endereco", "value"),
     State("clinica-telefone", "value"),
     State("clinica-email", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def add_clinica(n_clicks, cod, nome, endereco, telefone, email, current_refresh):
    if n_clicks and cod and nome:
        query = "INSERT INTO Clinica (CodCli, NomeCli, Endereco, Telefone, Email) VALUES (%s, %s, %s, %s, %s)"
        if execute_update(query, (cod, nome, endereco, telefone, email)):
            return dbc.Alert("Clínica cadastrada com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao cadastrar clínica!", color="danger"), current_refresh
    return "", current_refresh

@app.callback(
    [Output("clinica-edit-nome", "value"),
     Output("clinica-edit-endereco", "value"),
     Output("clinica-edit-telefone", "value"),
     Output("clinica-edit-email", "value"),
     Output("clinica-edit-nome", "disabled"),
     Output("clinica-edit-endereco", "disabled"),
     Output("clinica-edit-telefone", "disabled"),
     Output("clinica-edit-email", "disabled"),
     Output("btn-update-clinica", "disabled"),
     Output("msg-edit-clinica", "children")],
    Input("btn-search-clinica", "n_clicks"),
    State("clinica-edit-cod", "value"),
    prevent_initial_call=True
)
def search_clinica(n_clicks, cod):
    if n_clicks and cod:
        result = execute_query("SELECT * FROM Clinica WHERE CodCli = %s", (cod,))
        if result:
            c = result[0]
            return (c['NomeCli'], c['Endereco'], c['Telefone'], c['Email'],
                   False, False, False, False, False,
                   dbc.Alert(f"Clínica {cod} encontrada! Altere os campos desejados.", color="success"))
        return ("", "", "", "", True, True, True, True, True,
               dbc.Alert(f"Clínica com código {cod} não encontrada!", color="danger"))
    return "", "", "", "", True, True, True, True, True, ""

@app.callback(
    [Output("msg-edit-clinica", "children", allow_duplicate=True),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-update-clinica", "n_clicks"),
    [State("clinica-edit-cod", "value"),
     State("clinica-edit-nome", "value"),
     State("clinica-edit-endereco", "value"),
     State("clinica-edit-telefone", "value"),
     State("clinica-edit-email", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def update_clinica(n_clicks, cod, nome, endereco, telefone, email, current_refresh):
    if n_clicks and cod and nome:
        query = "UPDATE Clinica SET NomeCli = %s, Endereco = %s, Telefone = %s, Email = %s WHERE CodCli = %s"
        if execute_update(query, (nome, endereco, telefone, email, cod)):
            return dbc.Alert("Clínica atualizada com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao atualizar clínica!", color="danger"), current_refresh
    return "", current_refresh

@app.callback(
    [Output("clinica-delete-info", "children"),
     Output("btn-delete-clinica", "disabled")],
    Input("btn-search-delete-clinica", "n_clicks"),
    State("clinica-delete-cod", "value"),
    prevent_initial_call=True
)
def search_delete_clinica(n_clicks, cod):
    if n_clicks and cod:
        result = execute_query("SELECT * FROM Clinica WHERE CodCli = %s", (cod,))
        if result:
            c = result[0]
            info = dbc.Card([
                dbc.CardHeader("Dados da Clínica a ser Excluída", className="bg-danger text-white"),
                dbc.CardBody([
                    html.P([html.Strong("Código: "), c['CodCli']]),
                    html.P([html.Strong("Nome: "), c['NomeCli']]),
                    html.P([html.Strong("Endereço: "), c['Endereco'] or "N/A"]),
                    html.P([html.Strong("Telefone: "), c['Telefone'] or "N/A"]),
                    html.P([html.Strong("Email: "), c['Email'] or "N/A"]),
                    html.Hr(),
                    dbc.Alert([
                        html.I(className="bi bi-exclamation-triangle-fill me-2"),
                        "ATENÇÃO: Todas as consultas vinculadas a esta clínica também serão excluídas!"
                    ], color="warning", className="mb-0")
                ])
            ])
            return info, False
        return dbc.Alert(f"Clínica com código {cod} não encontrada!", color="danger"), True
    return dbc.Alert("Digite um código e clique em Buscar.", color="info"), True

@app.callback(
    [Output("msg-delete-clinica", "children"),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-delete-clinica", "n_clicks"),
    [State("clinica-delete-cod", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def delete_clinica(n_clicks, cod, current_refresh):
    if n_clicks and cod:
        query = "DELETE FROM Clinica WHERE CodCli = %s"
        if execute_update(query, (cod,)):
            return dbc.Alert("Clínica excluída com sucesso! (Consultas vinculadas também foram removidas)", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao excluir clínica!", color="danger"), current_refresh
    return "", current_refresh

# ==================== MÉDICOS ====================
def render_medicos():
    medicos = execute_query("SELECT * FROM Medico")
    df = pd.DataFrame(medicos) if medicos else pd.DataFrame()
    
    return html.Div([
        html.H3("Gestão de Médicos", className="mb-4"),
        dbc.Tabs(active_tab="tab-listar-medicos", children=[
            dbc.Tab(label="Listar", tab_id="tab-listar-medicos", children=[
                html.Div([
                    dash_table.DataTable(
                        id='table-medicos',
                        columns=[{"name": i, "id": i} for i in df.columns] if not df.empty else [],
                        data=df.to_dict('records') if not df.empty else [],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                    )
                ], className="mt-3")
            ]),
            dbc.Tab(label="Adicionar", tab_id="tab-adicionar-medicos", children=[
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Código"),
                            dbc.Input(id="medico-cod", type="number")
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Nome do Médico"),
                            dbc.Input(id="medico-nome", type="text")
                        ], width=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Gênero"),
                            dcc.Dropdown(id="medico-genero", options=[
                                {'label': 'Masculino', 'value': 'M'},
                                {'label': 'Feminino', 'value': 'F'}
                            ])
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Telefone"),
                            dbc.Input(id="medico-telefone", type="text")
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Email"),
                            dbc.Input(id="medico-email", type="email")
                        ], width=4),
                    ], className="mt-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Especialidade"),
                            dbc.Input(id="medico-especialidade", type="text")
                        ], width=6),
                    ], className="mt-3"),
                    dbc.Button("Cadastrar Médico", id="btn-add-medico", color="success", className="mt-3"),
                    html.Div(id="msg-medico", className="mt-3")
                ], className="mt-3")
            ]),
            dbc.Tab(label="Editar", tab_id="tab-editar-medicos", children=[
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Código do Médico"),
                            dbc.Input(id="medico-edit-cod", type="number", placeholder="Digite o código")
                        ], width=6),
                        dbc.Col([
                            dbc.Button("Buscar", id="btn-search-medico", color="info", className="mt-4")
                        ], width=2),
                    ]),
                    html.Hr(className="mt-3"),
                    html.Div(id="medico-edit-form", children=[
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Nome do Médico"),
                                dbc.Input(id="medico-edit-nome", type="text", disabled=True)
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Gênero"),
                                dcc.Dropdown(id="medico-edit-genero", options=[
                                    {'label': 'Masculino', 'value': 'M'},
                                    {'label': 'Feminino', 'value': 'F'}
                                ], disabled=True)
                            ], width=6),
                        ], className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Telefone"),
                                dbc.Input(id="medico-edit-telefone", type="text", disabled=True)
                            ], width=4),
                            dbc.Col([
                                dbc.Label("Email"),
                                dbc.Input(id="medico-edit-email", type="email", disabled=True)
                            ], width=4),
                            dbc.Col([
                                dbc.Label("Especialidade"),
                                dbc.Input(id="medico-edit-especialidade", type="text", disabled=True)
                            ], width=4),
                        ], className="mt-3"),
                        dbc.Button("Atualizar Médico", id="btn-update-medico", color="warning", className="mt-3", disabled=True),
                    ]),
                    html.Div(id="msg-edit-medico", className="mt-3")
                ], className="mt-3")
            ]),
            dbc.Tab(label="Excluir", tab_id="tab-excluir-medicos", children=[
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Código do Médico"),
                            dbc.Input(id="medico-delete-cod", type="number", placeholder="Digite o código")
                        ], width=6),
                        dbc.Col([
                            dbc.Button("Buscar", id="btn-search-delete-medico", color="info", className="mt-4")
                        ], width=2),
                    ]),
                    html.Hr(className="mt-3"),
                    html.Div(id="medico-delete-info", children=[
                        dbc.Alert("Digite um código e clique em Buscar para visualizar os dados.", color="info")
                    ]),
                    dbc.Button("Confirmar Exclusão", id="btn-delete-medico", color="danger", className="mt-3", disabled=True),
                    html.Div(id="msg-delete-medico", className="mt-3")
                ], className="mt-3")
            ]),
        ])
    ])

@app.callback(
    [Output("msg-medico", "children"),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-add-medico", "n_clicks"),
    [State("medico-cod", "value"),
     State("medico-nome", "value"),
     State("medico-genero", "value"),
     State("medico-telefone", "value"),
     State("medico-email", "value"),
     State("medico-especialidade", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def add_medico(n_clicks, cod, nome, genero, telefone, email, especialidade, current_refresh):
    if n_clicks and cod and nome:
        query = "INSERT INTO Medico (CodMed, NomeMed, Genero, Telefone, Email, Especialidade) VALUES (%s, %s, %s, %s, %s, %s)"
        if execute_update(query, (cod, nome, genero, telefone, email, especialidade)):
            return dbc.Alert("Médico cadastrado com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao cadastrar médico!", color="danger"), current_refresh
    return "", current_refresh

@app.callback(
    [Output("medico-edit-nome", "value"),
     Output("medico-edit-genero", "value"),
     Output("medico-edit-telefone", "value"),
     Output("medico-edit-email", "value"),
     Output("medico-edit-especialidade", "value"),
     Output("medico-edit-nome", "disabled"),
     Output("medico-edit-genero", "disabled"),
     Output("medico-edit-telefone", "disabled"),
     Output("medico-edit-email", "disabled"),
     Output("medico-edit-especialidade", "disabled"),
     Output("btn-update-medico", "disabled"),
     Output("msg-edit-medico", "children")],
    Input("btn-search-medico", "n_clicks"),
    State("medico-edit-cod", "value"),
    prevent_initial_call=True
)
def search_medico(n_clicks, cod):
    if n_clicks and cod:
        result = execute_query("SELECT * FROM Medico WHERE CodMed = %s", (cod,))
        if result:
            m = result[0]
            return (m['NomeMed'], m['Genero'], m['Telefone'], m['Email'], m['Especialidade'],
                   False, False, False, False, False, False,
                   dbc.Alert(f"Médico {cod} encontrado! Altere os campos desejados.", color="success"))
        return ("", "", "", "", "", True, True, True, True, True, True,
               dbc.Alert(f"Médico com código {cod} não encontrado!", color="danger"))
    return "", "", "", "", "", True, True, True, True, True, True, ""

@app.callback(
    [Output("msg-edit-medico", "children", allow_duplicate=True),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-update-medico", "n_clicks"),
    [State("medico-edit-cod", "value"),
     State("medico-edit-nome", "value"),
     State("medico-edit-genero", "value"),
     State("medico-edit-telefone", "value"),
     State("medico-edit-email", "value"),
     State("medico-edit-especialidade", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def update_medico(n_clicks, cod, nome, genero, telefone, email, especialidade, current_refresh):
    if n_clicks and cod and nome:
        query = "UPDATE Medico SET NomeMed = %s, Genero = %s, Telefone = %s, Email = %s, Especialidade = %s WHERE CodMed = %s"
        if execute_update(query, (nome, genero, telefone, email, especialidade, cod)):
            return dbc.Alert("Médico atualizado com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao atualizar médico!", color="danger"), current_refresh
    return "", current_refresh

@app.callback(
    [Output("medico-delete-info", "children"),
     Output("btn-delete-medico", "disabled")],
    Input("btn-search-delete-medico", "n_clicks"),
    State("medico-delete-cod", "value"),
    prevent_initial_call=True
)
def search_delete_medico(n_clicks, cod):
    if n_clicks and cod:
        result = execute_query("SELECT * FROM Medico WHERE CodMed = %s", (cod,))
        if result:
            m = result[0]
            info = dbc.Card([
                dbc.CardHeader("Dados do Médico a ser Excluído", className="bg-danger text-white"),
                dbc.CardBody([
                    html.P([html.Strong("Código: "), str(m['CodMed'])]),
                    html.P([html.Strong("Nome: "), m['NomeMed']]),
                    html.P([html.Strong("Gênero: "), m['Genero'] or "N/A"]),
                    html.P([html.Strong("Telefone: "), m['Telefone'] or "N/A"]),
                    html.P([html.Strong("Email: "), m['Email'] or "N/A"]),
                    html.P([html.Strong("Especialidade: "), m['Especialidade'] or "N/A"]),
                    html.Hr(),
                    dbc.Alert([
                        html.I(className="bi bi-exclamation-triangle-fill me-2"),
                        "ATENÇÃO: Todas as consultas vinculadas a este médico também serão excluídas!"
                    ], color="warning", className="mb-0")
                ])
            ])
            return info, False
        return dbc.Alert(f"Médico com código {cod} não encontrado!", color="danger"), True
    return dbc.Alert("Digite um código e clique em Buscar.", color="info"), True

@app.callback(
    [Output("msg-delete-medico", "children"),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-delete-medico", "n_clicks"),
    [State("medico-delete-cod", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def delete_medico(n_clicks, cod, current_refresh):
    if n_clicks and cod:
        query = "DELETE FROM Medico WHERE CodMed = %s"
        if execute_update(query, (cod,)):
            return dbc.Alert("Médico excluído com sucesso! (Consultas vinculadas também foram removidas)", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao excluir médico!", color="danger"), current_refresh
    return "", current_refresh

# ==================== PACIENTES ====================
def render_pacientes():
    pacientes = execute_query("SELECT * FROM Paciente")
    df = pd.DataFrame(pacientes) if pacientes else pd.DataFrame()
    
    return html.Div([
        html.H3("Gestão de Pacientes", className="mb-4"),
        dbc.Tabs(active_tab="tab-listar-pacientes", children=[
            dbc.Tab(label="Listar", tab_id="tab-listar-pacientes", children=[
                html.Div([
                    dash_table.DataTable(
                        id='table-pacientes',
                        columns=[{"name": i, "id": i} for i in df.columns] if not df.empty else [],
                        data=df.to_dict('records') if not df.empty else [],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                    )
                ], className="mt-3")
            ]),
            dbc.Tab(label="Adicionar", tab_id="tab-adicionar-pacientes", children=[
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("CPF (11 dígitos)"),
                            dbc.Input(id="paciente-cpf", type="text", maxLength=11)
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Nome do Paciente"),
                            dbc.Input(id="paciente-nome", type="text")
                        ], width=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Data de Nascimento"),
                            dbc.Input(id="paciente-data-nasc", type="date")
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Gênero"),
                            dcc.Dropdown(id="paciente-genero", options=[
                                {'label': 'Masculino', 'value': 'M'},
                                {'label': 'Feminino', 'value': 'F'}
                            ])
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Telefone"),
                            dbc.Input(id="paciente-telefone", type="text")
                        ], width=4),
                    ], className="mt-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Email"),
                            dbc.Input(id="paciente-email", type="email")
                        ], width=6),
                    ], className="mt-3"),
                    dbc.Button("Cadastrar Paciente", id="btn-add-paciente", color="info", className="mt-3"),
                    html.Div(id="msg-paciente", className="mt-3")
                ], className="mt-3")
            ]),
            dbc.Tab(label="Editar", tab_id="tab-editar-pacientes", children=[
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("CPF do Paciente (11 dígitos)"),
                            dbc.Input(id="paciente-edit-cpf", type="text", maxLength=11, placeholder="Digite o CPF")
                        ], width=6),
                        dbc.Col([
                            dbc.Button("Buscar", id="btn-search-paciente", color="info", className="mt-4")
                        ], width=2),
                    ]),
                    html.Hr(className="mt-3"),
                    html.Div(id="paciente-edit-form", children=[
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Nome do Paciente"),
                                dbc.Input(id="paciente-edit-nome", type="text", disabled=True)
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Data de Nascimento"),
                                dbc.Input(id="paciente-edit-data-nasc", type="date", disabled=True)
                            ], width=6),
                        ], className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Gênero"),
                                dcc.Dropdown(id="paciente-edit-genero", options=[
                                    {'label': 'Masculino', 'value': 'M'},
                                    {'label': 'Feminino', 'value': 'F'}
                                ], disabled=True)
                            ], width=4),
                            dbc.Col([
                                dbc.Label("Telefone"),
                                dbc.Input(id="paciente-edit-telefone", type="text", disabled=True)
                            ], width=4),
                            dbc.Col([
                                dbc.Label("Email"),
                                dbc.Input(id="paciente-edit-email", type="email", disabled=True)
                            ], width=4),
                        ], className="mt-3"),
                        dbc.Button("Atualizar Paciente", id="btn-update-paciente", color="warning", className="mt-3", disabled=True),
                    ]),
                    html.Div(id="msg-edit-paciente", className="mt-3")
                ], className="mt-3")
            ]),
            dbc.Tab(label="Excluir", tab_id="tab-excluir-pacientes", children=[
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("CPF do Paciente (11 dígitos)"),
                            dbc.Input(id="paciente-delete-cpf", type="text", maxLength=11, placeholder="Digite o CPF")
                        ], width=6),
                        dbc.Col([
                            dbc.Button("Buscar", id="btn-search-delete-paciente", color="info", className="mt-4")
                        ], width=2),
                    ]),
                    html.Hr(className="mt-3"),
                    html.Div(id="paciente-delete-info", children=[
                        dbc.Alert("Digite um CPF e clique em Buscar para visualizar os dados.", color="info")
                    ]),
                    dbc.Button("Confirmar Exclusão", id="btn-delete-paciente", color="danger", className="mt-3", disabled=True),
                    html.Div(id="msg-delete-paciente", className="mt-3")
                ], className="mt-3")
            ]),
        ])
    ])

@app.callback(
    [Output("msg-paciente", "children"),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-add-paciente", "n_clicks"),
    [State("paciente-cpf", "value"),
     State("paciente-nome", "value"),
     State("paciente-data-nasc", "value"),
     State("paciente-genero", "value"),
     State("paciente-telefone", "value"),
     State("paciente-email", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def add_paciente(n_clicks, cpf, nome, data_nasc, genero, telefone, email, current_refresh):
    if n_clicks and cpf and nome:
        query = "INSERT INTO Paciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email) VALUES (%s, %s, %s, %s, %s, %s)"
        if execute_update(query, (cpf, nome, data_nasc, genero, telefone, email)):
            return dbc.Alert("Paciente cadastrado com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao cadastrar paciente!", color="danger"), current_refresh
    return "", current_refresh

@app.callback(
    [Output("paciente-edit-nome", "value"),
     Output("paciente-edit-data-nasc", "value"),
     Output("paciente-edit-genero", "value"),
     Output("paciente-edit-telefone", "value"),
     Output("paciente-edit-email", "value"),
     Output("paciente-edit-nome", "disabled"),
     Output("paciente-edit-data-nasc", "disabled"),
     Output("paciente-edit-genero", "disabled"),
     Output("paciente-edit-telefone", "disabled"),
     Output("paciente-edit-email", "disabled"),
     Output("btn-update-paciente", "disabled"),
     Output("msg-edit-paciente", "children")],
    Input("btn-search-paciente", "n_clicks"),
    State("paciente-edit-cpf", "value"),
    prevent_initial_call=True
)
def search_paciente(n_clicks, cpf):
    if n_clicks and cpf:
        result = execute_query("SELECT * FROM Paciente WHERE CpfPaciente = %s", (cpf,))
        if result:
            p = result[0]
            return (p['NomePac'], str(p['DataNascimento']), p['Genero'], p['Telefone'], p['Email'],
                   False, False, False, False, False, False,
                   dbc.Alert(f"Paciente com CPF {cpf} encontrado! Altere os campos desejados.", color="success"))
        return ("", "", "", "", "", True, True, True, True, True, True,
               dbc.Alert(f"Paciente com CPF {cpf} não encontrado!", color="danger"))
    return "", "", "", "", "", True, True, True, True, True, True, ""

@app.callback(
    [Output("msg-edit-paciente", "children", allow_duplicate=True),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-update-paciente", "n_clicks"),
    [State("paciente-edit-cpf", "value"),
     State("paciente-edit-nome", "value"),
     State("paciente-edit-data-nasc", "value"),
     State("paciente-edit-genero", "value"),
     State("paciente-edit-telefone", "value"),
     State("paciente-edit-email", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def update_paciente(n_clicks, cpf, nome, data_nasc, genero, telefone, email, current_refresh):
    if n_clicks and cpf and nome:
        query = "UPDATE Paciente SET NomePac = %s, DataNascimento = %s, Genero = %s, Telefone = %s, Email = %s WHERE CpfPaciente = %s"
        if execute_update(query, (nome, data_nasc, genero, telefone, email, cpf)):
            return dbc.Alert("Paciente atualizado com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao atualizar paciente!", color="danger"), current_refresh
    return "", current_refresh

@app.callback(
    [Output("paciente-delete-info", "children"),
     Output("btn-delete-paciente", "disabled")],
    Input("btn-search-delete-paciente", "n_clicks"),
    State("paciente-delete-cpf", "value"),
    prevent_initial_call=True
)
def search_delete_paciente(n_clicks, cpf):
    if n_clicks and cpf:
        result = execute_query("SELECT * FROM Paciente WHERE CpfPaciente = %s", (cpf,))
        if result:
            p = result[0]
            info = dbc.Card([
                dbc.CardHeader("Dados do Paciente a ser Excluído", className="bg-danger text-white"),
                dbc.CardBody([
                    html.P([html.Strong("CPF: "), p['CpfPaciente']]),
                    html.P([html.Strong("Nome: "), p['NomePac']]),
                    html.P([html.Strong("Data de Nascimento: "), str(p['DataNascimento'])]),
                    html.P([html.Strong("Gênero: "), p['Genero'] or "N/A"]),
                    html.P([html.Strong("Telefone: "), p['Telefone'] or "N/A"]),
                    html.P([html.Strong("Email: "), p['Email'] or "N/A"]),
                    html.Hr(),
                    dbc.Alert([
                        html.I(className="bi bi-exclamation-triangle-fill me-2"),
                        "ATENÇÃO: Todas as consultas vinculadas a este paciente também serão excluídas!"
                    ], color="warning", className="mb-0")
                ])
            ])
            return info, False
        return dbc.Alert(f"Paciente com CPF {cpf} não encontrado!", color="danger"), True
    return dbc.Alert("Digite um CPF e clique em Buscar.", color="info"), True

@app.callback(
    [Output("msg-delete-paciente", "children"),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-delete-paciente", "n_clicks"),
    [State("paciente-delete-cpf", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def delete_paciente(n_clicks, cpf, current_refresh):
    if n_clicks and cpf:
        query = "DELETE FROM Paciente WHERE CpfPaciente = %s"
        if execute_update(query, (cpf,)):
            return dbc.Alert("Paciente excluído com sucesso! (Consultas vinculadas também foram removidas)", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao excluir paciente!", color="danger"), current_refresh
    return "", current_refresh

# ==================== CONSULTAS ====================
def render_consultas():
    consultas = execute_query("""
        SELECT c.CodCli, cl.NomeCli, c.CodMed, m.NomeMed, c.CpfPaciente, p.NomePac, c.Data_Hora
        FROM Consulta c
        JOIN Clinica cl ON c.CodCli = cl.CodCli
        JOIN Medico m ON c.CodMed = m.CodMed
        JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
        ORDER BY c.Data_Hora
    """)
    df = pd.DataFrame(consultas) if consultas else pd.DataFrame()
    
    clinicas = execute_query("SELECT CodCli, NomeCli FROM Clinica")
    medicos = execute_query("SELECT CodMed, NomeMed FROM Medico")
    pacientes = execute_query("SELECT CpfPaciente, NomePac FROM Paciente")
    
    return html.Div([
        html.H3("Gestão de Consultas", className="mb-4"),
        dbc.Tabs(active_tab="tab-listar-consultas", children=[
            dbc.Tab(label="Listar", tab_id="tab-listar-consultas", children=[
                html.Div([
                    dash_table.DataTable(
                        id='table-consultas',
                        columns=[{"name": i, "id": i} for i in df.columns] if not df.empty else [],
                        data=df.to_dict('records') if not df.empty else [],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                    )
                ], className="mt-3")
            ]),
            dbc.Tab(label="Adicionar", tab_id="tab-adicionar-consultas", children=[
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Clínica"),
                            dcc.Dropdown(
                                id="consulta-clinica",
                                options=[{'label': c['NomeCli'], 'value': c['CodCli']} for c in clinicas] if clinicas else []
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Médico"),
                            dcc.Dropdown(
                                id="consulta-medico",
                                options=[{'label': m['NomeMed'], 'value': m['CodMed']} for m in medicos] if medicos else []
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Paciente"),
                            dcc.Dropdown(
                                id="consulta-paciente",
                                options=[{'label': p['NomePac'], 'value': p['CpfPaciente']} for p in pacientes] if pacientes else []
                            )
                        ], width=4),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Data"),
                            dbc.Input(id="consulta-data", type="date")
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Hora"),
                            dbc.Input(id="consulta-hora", type="time")
                        ], width=6),
                    ], className="mt-3"),
                    dbc.Button("Agendar Consulta", id="btn-add-consulta", color="warning", className="mt-3"),
                    html.Div(id="msg-consulta", className="mt-3")
                ], className="mt-3")
            ]),
            dbc.Tab(label="Editar", tab_id="tab-editar-consultas", children=[
                dbc.Form([
                    html.H5("Digite a Chave Primária da Consulta"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Código da Clínica"),
                            dbc.Input(id="consulta-edit-codcli", type="text", maxLength=7, placeholder="Ex: 0000001")
                        ], width=3),
                        dbc.Col([
                            dbc.Label("Código do Médico"),
                            dbc.Input(id="consulta-edit-codmed", type="number", placeholder="Ex: 2819374")
                        ], width=3),
                        dbc.Col([
                            dbc.Label("CPF do Paciente"),
                            dbc.Input(id="consulta-edit-cpfpac", type="text", maxLength=11, placeholder="Ex: 34512389765")
                        ], width=3),
                        dbc.Col([
                            dbc.Label("Data/Hora Atual"),
                            dbc.Input(id="consulta-edit-datahora-antiga", type="text", placeholder="YYYY-MM-DD HH:MM:SS")
                        ], width=3),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Buscar", id="btn-search-consulta", color="info", className="mt-3")
                        ], width=2),
                    ]),
                    html.Hr(className="mt-3"),
                    html.Div(id="consulta-edit-form", children=[
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Nova Data"),
                                dbc.Input(id="consulta-edit-data", type="date", disabled=True)
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Nova Hora"),
                                dbc.Input(id="consulta-edit-hora", type="time", disabled=True)
                            ], width=6),
                        ], className="mt-3"),
                        dbc.Button("Atualizar Consulta", id="btn-update-consulta", color="warning", className="mt-3", disabled=True),
                    ]),
                    html.Div(id="msg-edit-consulta", className="mt-3")
                ], className="mt-3")
            ]),
            dbc.Tab(label="Excluir", tab_id="tab-excluir-consultas", children=[
                dbc.Form([
                    html.H5("Digite a Chave Primária da Consulta"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Código da Clínica"),
                            dbc.Input(id="consulta-delete-codcli", type="text", maxLength=7, placeholder="Ex: 0000001")
                        ], width=3),
                        dbc.Col([
                            dbc.Label("Código do Médico"),
                            dbc.Input(id="consulta-delete-codmed", type="number", placeholder="Ex: 2819374")
                        ], width=3),
                        dbc.Col([
                            dbc.Label("CPF do Paciente"),
                            dbc.Input(id="consulta-delete-cpfpac", type="text", maxLength=11, placeholder="Ex: 34512389765")
                        ], width=3),
                        dbc.Col([
                            dbc.Label("Data/Hora"),
                            dbc.Input(id="consulta-delete-datahora", type="text", placeholder="YYYY-MM-DD HH:MM:SS")
                        ], width=3),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Buscar", id="btn-search-delete-consulta", color="info", className="mt-3")
                        ], width=2),
                    ]),
                    html.Hr(className="mt-3"),
                    html.Div(id="consulta-delete-info", children=[
                        dbc.Alert("Digite a chave primária completa e clique em Buscar.", color="info")
                    ]),
                    dbc.Button("Confirmar Exclusão", id="btn-delete-consulta", color="danger", className="mt-3", disabled=True),
                    html.Div(id="msg-delete-consulta", className="mt-3")
                ], className="mt-3")
            ]),
        ])
    ])

@app.callback(
    [Output("msg-consulta", "children"),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-add-consulta", "n_clicks"),
    [State("consulta-clinica", "value"),
     State("consulta-medico", "value"),
     State("consulta-paciente", "value"),
     State("consulta-data", "value"),
     State("consulta-hora", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def add_consulta(n_clicks, clinica, medico, paciente, data, hora, current_refresh):
    if n_clicks and clinica and medico and paciente and data and hora:
        data_hora = f"{data} {hora}:00"
        query = "INSERT INTO Consulta (CodCli, CodMed, CpfPaciente, Data_Hora) VALUES (%s, %s, %s, %s)"
        if execute_update(query, (clinica, medico, paciente, data_hora)):
            return dbc.Alert("Consulta agendada com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao agendar consulta!", color="danger"), current_refresh
    return "", current_refresh

@app.callback(
    [Output("consulta-edit-data", "value"),
     Output("consulta-edit-hora", "value"),
     Output("consulta-edit-data", "disabled"),
     Output("consulta-edit-hora", "disabled"),
     Output("btn-update-consulta", "disabled"),
     Output("msg-edit-consulta", "children")],
    Input("btn-search-consulta", "n_clicks"),
    [State("consulta-edit-codcli", "value"),
     State("consulta-edit-codmed", "value"),
     State("consulta-edit-cpfpac", "value"),
     State("consulta-edit-datahora-antiga", "value")],
    prevent_initial_call=True
)
def search_consulta(n_clicks, cod_cli, cod_med, cpf_pac, data_hora_antiga):
    if n_clicks and cod_cli and cod_med and cpf_pac and data_hora_antiga:
        query = """SELECT * FROM Consulta 
                   WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s AND Data_Hora = %s"""
        result = execute_query(query, (cod_cli, cod_med, cpf_pac, data_hora_antiga))
        if result:
            c = result[0]
            data_hora_str = str(c['Data_Hora'])
            data = data_hora_str.split(' ')[0]
            hora = data_hora_str.split(' ')[1][:5]
            return (data, hora, False, False, False,
                   dbc.Alert("Consulta encontrada! Altere a data/hora desejada.", color="success"))
        return ("", "", True, True, True,
               dbc.Alert("Consulta não encontrada! Verifique a chave primária.", color="danger"))
    return "", "", True, True, True, ""

@app.callback(
    [Output("msg-edit-consulta", "children", allow_duplicate=True),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-update-consulta", "n_clicks"),
    [State("consulta-edit-codcli", "value"),
     State("consulta-edit-codmed", "value"),
     State("consulta-edit-cpfpac", "value"),
     State("consulta-edit-datahora-antiga", "value"),
     State("consulta-edit-data", "value"),
     State("consulta-edit-hora", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def update_consulta(n_clicks, cod_cli, cod_med, cpf_pac, data_hora_antiga, nova_data, nova_hora, current_refresh):
    if n_clicks and cod_cli and cod_med and cpf_pac and data_hora_antiga and nova_data and nova_hora:
        nova_data_hora = f"{nova_data} {nova_hora}:00"
        query = "UPDATE Consulta SET Data_Hora = %s WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s AND Data_Hora = %s"
        if execute_update(query, (nova_data_hora, cod_cli, cod_med, cpf_pac, data_hora_antiga)):
            return dbc.Alert("Consulta atualizada com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao atualizar consulta!", color="danger"), current_refresh
    return "", current_refresh

@app.callback(
    [Output("consulta-delete-info", "children"),
     Output("btn-delete-consulta", "disabled")],
    Input("btn-search-delete-consulta", "n_clicks"),
    [State("consulta-delete-codcli", "value"),
     State("consulta-delete-codmed", "value"),
     State("consulta-delete-cpfpac", "value"),
     State("consulta-delete-datahora", "value")],
    prevent_initial_call=True
)
def search_delete_consulta(n_clicks, cod_cli, cod_med, cpf_pac, data_hora):
    if n_clicks and cod_cli and cod_med and cpf_pac and data_hora:
        query = """SELECT c.*, cl.NomeCli, m.NomeMed, p.NomePac
                   FROM Consulta c
                   JOIN Clinica cl ON c.CodCli = cl.CodCli
                   JOIN Medico m ON c.CodMed = m.CodMed
                   JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
                   WHERE c.CodCli = %s AND c.CodMed = %s AND c.CpfPaciente = %s AND c.Data_Hora = %s"""
        result = execute_query(query, (cod_cli, cod_med, cpf_pac, data_hora))
        if result:
            c = result[0]
            info = dbc.Card([
                dbc.CardHeader("Dados da Consulta a ser Excluída", className="bg-danger text-white"),
                dbc.CardBody([
                    html.P([html.Strong("Clínica: "), f"{c['CodCli']} - {c['NomeCli']}"]),
                    html.P([html.Strong("Médico: "), f"{c['CodMed']} - {c['NomeMed']}"]),
                    html.P([html.Strong("Paciente: "), f"{c['CpfPaciente']} - {c['NomePac']}"]),
                    html.P([html.Strong("Data/Hora: "), str(c['Data_Hora'])]),
                ])
            ])
            return info, False
        return dbc.Alert("Consulta não encontrada! Verifique a chave primária.", color="danger"), True
    return dbc.Alert("Digite a chave primária completa e clique em Buscar.", color="info"), True

@app.callback(
    [Output("msg-delete-consulta", "children"),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-delete-consulta", "n_clicks"),
    [State("consulta-delete-codcli", "value"),
     State("consulta-delete-codmed", "value"),
     State("consulta-delete-cpfpac", "value"),
     State("consulta-delete-datahora", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def delete_consulta(n_clicks, cod_cli, cod_med, cpf_pac, data_hora, current_refresh):
    if n_clicks and cod_cli and cod_med and cpf_pac and data_hora:
        query = "DELETE FROM Consulta WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s AND Data_Hora = %s"
        if execute_update(query, (cod_cli, cod_med, cpf_pac, data_hora)):
            return dbc.Alert("Consulta excluída com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao excluir consulta!", color="danger"), current_refresh
    return "", current_refresh

if __name__ == '__main__':
    app.run(debug=True)
