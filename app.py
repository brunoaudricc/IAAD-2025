import dash
from dash import dcc, html, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
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
                margin-bottom: -2px !important;
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
        connection = mysql.connector.connect(**DB_CONFIG)
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
                dbc.NavLink([html.I(className="fas fa-clock me-2"), "Lista de Espera"], href="#", id="tab-lista-espera"),
                dbc.NavLink([html.I(className="fas fa-chart-pie me-2"), "Gráficos"], href="#", id="tab-graficos"),
            ], pills=True, className="mb-4", justified=True)
        ], lg=11, md=12)
    ], justify="center"),
    
    # Conteúdo centralizado
    dbc.Row([
        dbc.Col([
            html.Div(id="tab-content", className="p-3")
        ], lg=11, md=12)
    ], justify="center"),
    
    dcc.Store(id='refresh-trigger', data=0),
    dcc.Store(id='active-tab', data='home'),
    dcc.Store(id='consulta-edit-selected-data', data=None),
    dcc.Store(id='consulta-delete-selected-data', data=None)
], fluid=True, className="px-4")

# Callback para controlar navegação
@app.callback(
    [Output('active-tab', 'data'),
     Output('tab-home', 'active'),
     Output('tab-clinicas', 'active'),
     Output('tab-medicos', 'active'),
     Output('tab-pacientes', 'active'),
     Output('tab-consultas', 'active'),
     Output('tab-lista-espera', 'active'),
     Output('tab-graficos', 'active')],
    [Input('tab-home', 'n_clicks'),
     Input('tab-clinicas', 'n_clicks'),
     Input('tab-medicos', 'n_clicks'),
     Input('tab-pacientes', 'n_clicks'),
     Input('tab-consultas', 'n_clicks'),
     Input('tab-lista-espera', 'n_clicks'),
     Input('tab-graficos', 'n_clicks')],
    prevent_initial_call=False
)
def update_active_tab(home_clicks, clinicas_clicks, medicos_clicks, pacientes_clicks, consultas_clicks, lista_espera_clicks, graficos_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return 'home', True, False, False, False, False, False, False
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    tabs = {
        'tab-home': ('home', [True, False, False, False, False, False, False]),
        'tab-clinicas': ('clinicas', [False, True, False, False, False, False, False]),
        'tab-medicos': ('medicos', [False, False, True, False, False, False, False]),
        'tab-pacientes': ('pacientes', [False, False, False, True, False, False, False]),
        'tab-consultas': ('consultas', [False, False, False, False, True, False, False]),
        'tab-lista-espera': ('lista-espera', [False, False, False, False, False, True, False]),
        'tab-graficos': ('graficos', [False, False, False, False, False, False, True])
    }
    
    if button_id in tabs:
        tab_name, active_states = tabs[button_id]
        return tab_name, *active_states
    
    return 'home', True, False, False, False, False, False, False

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
    elif active_tab == "lista-espera":
        return render_lista_espera()
    elif active_tab == "graficos":
        return render_graficos()
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
    medicos = execute_query("""
        SELECT m.CodMed, m.NomeMed, m.Genero, m.Especialidade, 
               m.Telefone, m.Email, COUNT(c.CodMed) as TotalConsultas
        FROM Medico m
        LEFT JOIN Consulta c ON m.CodMed = c.CodMed
        GROUP BY m.CodMed
        ORDER BY TotalConsultas DESC
    """)
    df = pd.DataFrame(medicos) if medicos else pd.DataFrame()
    
    especialidades = execute_query("SELECT DISTINCT Especialidade FROM Medico ORDER BY Especialidade")
    
    return html.Div([
        html.H3([
            html.I(className="fas fa-user-md me-3", style={'color': '#10b981'}),
            "Gestão de Médicos"
        ], className="mb-4"),
        dbc.Tabs(active_tab="tab-listar-medicos", children=[
            dbc.Tab(label="Listar", tab_id="tab-listar-medicos", children=[
                html.Div([
                    # Filtros Avançados
                    dbc.Card([
                        dbc.CardBody([
                            html.H5([html.I(className="fas fa-filter me-2"), "Filtros de Pesquisa"], className="mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Buscar por Nome"),
                                    dbc.Input(id="filtro-medico-nome", type="text", 
                                             placeholder="Digite o nome do médico...")
                                ], md=3),
                                dbc.Col([
                                    dbc.Label("Especialidade"),
                                    dcc.Dropdown(
                                        id="filtro-medico-especialidade",
                                        options=[{'label': 'Todas', 'value': 'all'}] + 
                                                [{'label': e['Especialidade'], 'value': e['Especialidade']} for e in especialidades] if especialidades else [],
                                        value='all',
                                        clearable=False
                                    )
                                ], md=2),
                                dbc.Col([
                                    dbc.Label("Gênero"),
                                    dcc.Dropdown(
                                        id="filtro-medico-genero",
                                        options=[
                                            {'label': 'Todos', 'value': 'all'},
                                            {'label': 'Masculino', 'value': 'M'},
                                            {'label': 'Feminino', 'value': 'F'}
                                        ],
                                        value='all',
                                        clearable=False
                                    )
                                ], md=2),
                                dbc.Col([
                                    dbc.Label("Ordenar por"),
                                    dcc.Dropdown(
                                        id="filtro-medico-ordenacao",
                                        options=[
                                            {'label': 'Mais Consultas', 'value': 'consultas_desc'},
                                            {'label': 'Menos Consultas', 'value': 'consultas_asc'},
                                            {'label': 'Nome (A-Z)', 'value': 'nome_asc'},
                                            {'label': 'Nome (Z-A)', 'value': 'nome_desc'}
                                        ],
                                        value='consultas_desc',
                                        clearable=False
                                    )
                                ], md=3),
                                dbc.Col([
                                    dbc.Label(html.Br()),
                                    dbc.Button([html.I(className="fas fa-search me-2"), "Filtrar"], 
                                              id="btn-filtrar-medicos", color="success", className="w-100")
                                ], md=2),
                            ])
                        ])
                    ], className="mb-3"),
                    
                    # Tabela de Resultados
                    html.Div(id="medicos-filtrados-container", children=[
                        dash_table.DataTable(
                            id='table-medicos',
                            columns=[{"name": i, "id": i} for i in df.columns] if not df.empty else [],
                            data=df.to_dict('records') if not df.empty else [],
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'padding': '10px'},
                            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                            page_size=15
                        )
                    ])
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

# Callback: Filtrar Médicos
@app.callback(
    Output("medicos-filtrados-container", "children"),
    [Input("btn-filtrar-medicos", "n_clicks"),
     Input("refresh-trigger", "data")],
    [State("filtro-medico-nome", "value"),
     State("filtro-medico-especialidade", "value"),
     State("filtro-medico-genero", "value"),
     State("filtro-medico-ordenacao", "value")],
    prevent_initial_call=False
)
def filtrar_medicos(n_clicks, refresh, nome, especialidade, genero, ordenacao):
    # Query com LEFT JOIN para incluir médicos sem consultas + COUNT + GROUP BY
    query = """
        SELECT m.CodMed as Codigo, m.NomeMed as Medico, 
               CASE 
                   WHEN m.Genero = 'M' THEN 'Masculino'
                   WHEN m.Genero = 'F' THEN 'Feminino'
                   ELSE 'Não informado'
               END as Genero,
               m.Especialidade, m.Telefone, m.Email,
               COUNT(c.CodMed) as TotalConsultas
        FROM Medico m
        LEFT JOIN Consulta c ON m.CodMed = c.CodMed
        WHERE 1=1
    """
    params = []
    
    # Filtro: Nome do Médico (LIKE para busca parcial)
    if nome and nome.strip():
        query += " AND m.NomeMed LIKE %s"
        params.append(f"%{nome}%")
    
    # Filtro: Especialidade
    if especialidade and especialidade != 'all':
        query += " AND m.Especialidade = %s"
        params.append(especialidade)
    
    # Filtro: Gênero
    if genero and genero != 'all':
        query += " AND m.Genero = %s"
        params.append(genero)
    
    query += " GROUP BY m.CodMed, m.NomeMed, m.Genero, m.Especialidade, m.Telefone, m.Email"
    
    # Ordenação dinâmica
    if ordenacao == 'consultas_desc':
        query += " ORDER BY TotalConsultas DESC, m.NomeMed ASC"
    elif ordenacao == 'consultas_asc':
        query += " ORDER BY TotalConsultas ASC, m.NomeMed ASC"
    elif ordenacao == 'nome_asc':
        query += " ORDER BY m.NomeMed ASC"
    elif ordenacao == 'nome_desc':
        query += " ORDER BY m.NomeMed DESC"
    
    medicos = execute_query(query, tuple(params) if params else None)
    df = pd.DataFrame(medicos) if medicos else pd.DataFrame()
    
    if df.empty:
        return dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "Nenhum médico encontrado com os filtros selecionados."
        ], color="info")
    
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        page_size=15,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {'filter_query': '{TotalConsultas} = 0'},
                'backgroundColor': '#fee2e2',
                'color': '#991b1b'
            }
        ]
    )

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
    pacientes = execute_query("""
        SELECT p.CpfPaciente, p.NomePac, 
               DATE_FORMAT(p.DataNascimento, '%d/%m/%Y') as DataNascimento,
               TIMESTAMPDIFF(YEAR, p.DataNascimento, CURDATE()) as Idade,
               CASE 
                   WHEN p.Genero = 'M' THEN 'Masculino'
                   WHEN p.Genero = 'F' THEN 'Feminino'
                   ELSE 'Não informado'
               END as Genero,
               p.Telefone, p.Email,
               COUNT(c.CpfPaciente) as TotalConsultas
        FROM Paciente p
        LEFT JOIN Consulta c ON p.CpfPaciente = c.CpfPaciente
        GROUP BY p.CpfPaciente
        ORDER BY p.NomePac
    """)
    df = pd.DataFrame(pacientes) if pacientes else pd.DataFrame()
    
    return html.Div([
        html.H3([
            html.I(className="fas fa-users me-3", style={'color': '#3b82f6'}),
            "Gestão de Pacientes"
        ], className="mb-4"),
        dbc.Tabs(active_tab="tab-listar-pacientes", children=[
            dbc.Tab(label="Listar", tab_id="tab-listar-pacientes", children=[
                html.Div([
                    # Filtros Avançados
                    dbc.Card([
                        dbc.CardBody([
                            html.H5([html.I(className="fas fa-filter me-2"), "Filtros de Pesquisa"], className="mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Buscar por Nome"),
                                    dbc.Input(id="filtro-paciente-nome", type="text", 
                                             placeholder="Digite o nome do paciente...")
                                ], md=3),
                                dbc.Col([
                                    dbc.Label("Faixa Etária"),
                                    dcc.Dropdown(
                                        id="filtro-paciente-faixa-etaria",
                                        options=[
                                            {'label': 'Todas as Idades', 'value': 'all'},
                                            {'label': 'Criança/Adolescente (0-17)', 'value': '0-17'},
                                            {'label': 'Jovem Adulto (18-35)', 'value': '18-35'},
                                            {'label': 'Adulto (36-59)', 'value': '36-59'},
                                            {'label': 'Idoso (60+)', 'value': '60-150'}
                                        ],
                                        value='all',
                                        clearable=False
                                    )
                                ], md=2),
                                dbc.Col([
                                    dbc.Label("Gênero"),
                                    dcc.Dropdown(
                                        id="filtro-paciente-genero",
                                        options=[
                                            {'label': 'Todos', 'value': 'all'},
                                            {'label': 'Masculino', 'value': 'M'},
                                            {'label': 'Feminino', 'value': 'F'}
                                        ],
                                        value='all',
                                        clearable=False
                                    )
                                ], md=2),
                                dbc.Col([
                                    dbc.Label("Consultas Mínimas"),
                                    dcc.Dropdown(
                                        id="filtro-paciente-min-consultas",
                                        options=[
                                            {'label': 'Todos', 'value': 0},
                                            {'label': 'Pelo menos 1', 'value': 1},
                                            {'label': 'Pelo menos 2', 'value': 2},
                                            {'label': 'Pelo menos 3', 'value': 3},
                                            {'label': 'Pelo menos 5', 'value': 5}
                                        ],
                                        value=0,
                                        clearable=False
                                    )
                                ], md=2),
                                dbc.Col([
                                    dbc.Label(html.Br()),
                                    dbc.Button([html.I(className="fas fa-search me-2"), "Filtrar"], 
                                              id="btn-filtrar-pacientes", color="primary", className="w-100")
                                ], md=3),
                            ])
                        ])
                    ], className="mb-3"),
                    
                    # Tabela de Resultados
                    html.Div(id="pacientes-filtrados-container", children=[
                        dash_table.DataTable(
                            id='table-pacientes',
                            columns=[{"name": i, "id": i} for i in df.columns] if not df.empty else [],
                            data=df.to_dict('records') if not df.empty else [],
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'padding': '10px'},
                            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                            page_size=15
                        )
                    ])
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

# Callback: Filtrar Pacientes
@app.callback(
    Output("pacientes-filtrados-container", "children"),
    [Input("btn-filtrar-pacientes", "n_clicks"),
     Input("refresh-trigger", "data")],
    [State("filtro-paciente-nome", "value"),
     State("filtro-paciente-faixa-etaria", "value"),
     State("filtro-paciente-genero", "value"),
     State("filtro-paciente-min-consultas", "value")],
    prevent_initial_call=False
)
def filtrar_pacientes(n_clicks, refresh, nome, faixa_etaria, genero, min_consultas):
    # Query com TIMESTAMPDIFF + LEFT JOIN + COUNT + HAVING
    query = """
        SELECT p.CpfPaciente as CPF, p.NomePac as Paciente,
               DATE_FORMAT(p.DataNascimento, '%d/%m/%Y') as DataNascimento,
               TIMESTAMPDIFF(YEAR, p.DataNascimento, CURDATE()) as Idade,
               CASE 
                   WHEN p.Genero = 'M' THEN 'Masculino'
                   WHEN p.Genero = 'F' THEN 'Feminino'
                   ELSE 'Não informado'
               END as Genero,
               p.Telefone, p.Email,
               COUNT(c.CpfPaciente) as TotalConsultas
        FROM Paciente p
        LEFT JOIN Consulta c ON p.CpfPaciente = c.CpfPaciente
        WHERE 1=1
    """
    params = []
    
    # Filtro: Nome do Paciente (LIKE para busca parcial)
    if nome and nome.strip():
        query += " AND p.NomePac LIKE %s"
        params.append(f"%{nome}%")
    
    # Filtro: Faixa Etária (usando TIMESTAMPDIFF)
    if faixa_etaria and faixa_etaria != 'all':
        idade_min, idade_max = map(int, faixa_etaria.split('-'))
        query += " AND TIMESTAMPDIFF(YEAR, p.DataNascimento, CURDATE()) BETWEEN %s AND %s"
        params.extend([idade_min, idade_max])
    
    # Filtro: Gênero
    if genero and genero != 'all':
        query += " AND p.Genero = %s"
        params.append(genero)
    
    query += " GROUP BY p.CpfPaciente, p.NomePac, p.DataNascimento, p.Genero, p.Telefone, p.Email"
    
    # Filtro: Consultas Mínimas (usando HAVING)
    if min_consultas and int(min_consultas) > 0:
        query += " HAVING COUNT(c.CpfPaciente) >= %s"
        params.append(int(min_consultas))
    
    query += " ORDER BY TotalConsultas DESC, p.NomePac ASC"
    
    pacientes = execute_query(query, tuple(params) if params else None)
    df = pd.DataFrame(pacientes) if pacientes else pd.DataFrame()
    
    if df.empty:
        return dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "Nenhum paciente encontrado com os filtros selecionados."
        ], color="info")
    
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        page_size=15,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {'filter_query': '{TotalConsultas} = 0'},
                'backgroundColor': '#fef3c7',
                'color': '#92400e'
            }
        ]
    )

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
        SELECT c.CodCli, cl.NomeCli as Clinica, c.CodMed, m.NomeMed as Medico, 
               m.Especialidade, c.CpfPaciente, p.NomePac as Paciente, c.Data_Hora
        FROM Consulta c
        JOIN Clinica cl ON c.CodCli = cl.CodCli
        JOIN Medico m ON c.CodMed = m.CodMed
        JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
        ORDER BY c.Data_Hora DESC
    """)
    df = pd.DataFrame(consultas) if consultas else pd.DataFrame()
    
    clinicas = execute_query("SELECT CodCli, NomeCli FROM Clinica")
    medicos = execute_query("SELECT CodMed, NomeMed FROM Medico")
    pacientes = execute_query("SELECT CpfPaciente, NomePac FROM Paciente")
    especialidades = execute_query("SELECT DISTINCT Especialidade FROM Medico ORDER BY Especialidade")
    
    return html.Div([
        html.H3([
            html.I(className="fas fa-calendar-check me-3", style={'color': '#0ea5e9'}),
            "Gestão de Consultas"
        ], className="mb-4"),
        dbc.Tabs(active_tab="tab-listar-consultas", children=[
            dbc.Tab(label="Listar", tab_id="tab-listar-consultas", children=[
                html.Div([
                    # Filtros Avançados
                    dbc.Card([
                        dbc.CardBody([
                            html.H5([html.I(className="fas fa-filter me-2"), "Filtros de Pesquisa"], className="mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Buscar Paciente"),
                                    dbc.Input(id="filtro-consulta-paciente", type="text", 
                                             placeholder="Digite o nome do paciente...")
                                ], md=3),
                                dbc.Col([
                                    dbc.Label("Clínica"),
                                    dcc.Dropdown(
                                        id="filtro-consulta-clinica",
                                        options=[{'label': 'Todas', 'value': 'all'}] + 
                                                [{'label': c['NomeCli'], 'value': c['CodCli']} for c in clinicas] if clinicas else [],
                                        value='all',
                                        clearable=False
                                    )
                                ], md=3),
                                dbc.Col([
                                    dbc.Label("Especialidade"),
                                    dcc.Dropdown(
                                        id="filtro-consulta-especialidade",
                                        options=[{'label': 'Todas', 'value': 'all'}] + 
                                                [{'label': e['Especialidade'], 'value': e['Especialidade']} for e in especialidades] if especialidades else [],
                                        value='all',
                                        clearable=False
                                    )
                                ], md=2),
                                dbc.Col([
                                    dbc.Label("Data Inicial"),
                                    dbc.Input(id="filtro-consulta-data-inicio", type="date")
                                ], md=2),
                                dbc.Col([
                                    dbc.Label("Data Final"),
                                    dbc.Input(id="filtro-consulta-data-fim", type="date")
                                ], md=2),
                            ]),
                            dbc.Button([html.I(className="fas fa-search me-2"), "Filtrar"], 
                                      id="btn-filtrar-consultas", color="primary", className="mt-3")
                        ])
                    ], className="mb-3"),
                    
                    # Tabela de Resultados
                    html.Div(id="consultas-filtradas-container", children=[
                        dash_table.DataTable(
                            id='table-consultas',
                            columns=[{"name": i, "id": i} for i in ['Clinica', 'Medico', 'Especialidade', 'Paciente', 'Data_Hora']] if not df.empty else [],
                            data=df[['Clinica', 'Medico', 'Especialidade', 'Paciente', 'Data_Hora']].to_dict('records') if not df.empty else [],
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'padding': '10px'},
                            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                            page_size=15
                        )
                    ])
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
                    html.Div(id="consulta-edit-results", className="mt-3"),
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
                    html.Div(id="consulta-delete-results", className="mt-3"),
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

# Callback: Filtrar Consultas
@app.callback(
    Output("consultas-filtradas-container", "children"),
    [Input("btn-filtrar-consultas", "n_clicks"),
     Input("refresh-trigger", "data")],
    [State("filtro-consulta-paciente", "value"),
     State("filtro-consulta-clinica", "value"),
     State("filtro-consulta-especialidade", "value"),
     State("filtro-consulta-data-inicio", "value"),
     State("filtro-consulta-data-fim", "value")],
    prevent_initial_call=False
)
def filtrar_consultas(n_clicks, refresh, nome_paciente, clinica, especialidade, data_inicio, data_fim):
    # Query base com JOINs
    query = """
        SELECT cl.NomeCli as Clinica, m.NomeMed as Medico, 
               m.Especialidade, p.NomePac as Paciente, 
               DATE_FORMAT(c.Data_Hora, '%d/%m/%Y %H:%i') as Data_Hora
        FROM Consulta c
        JOIN Clinica cl ON c.CodCli = cl.CodCli
        JOIN Medico m ON c.CodMed = m.CodMed
        JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
        WHERE 1=1
    """
    params = []
    
    # Filtro: Nome do Paciente (LIKE para busca parcial)
    if nome_paciente and nome_paciente.strip():
        query += " AND p.NomePac LIKE %s"
        params.append(f"%{nome_paciente}%")
    
    # Filtro: Clínica
    if clinica and clinica != 'all':
        query += " AND c.CodCli = %s"
        params.append(clinica)
    
    # Filtro: Especialidade
    if especialidade and especialidade != 'all':
        query += " AND m.Especialidade = %s"
        params.append(especialidade)
    
    # Filtro: Período (Data Inicial e Final)
    if data_inicio:
        query += " AND DATE(c.Data_Hora) >= %s"
        params.append(data_inicio)
    
    if data_fim:
        query += " AND DATE(c.Data_Hora) <= %s"
        params.append(data_fim)
    
    query += " ORDER BY c.Data_Hora DESC"
    
    # Executar query com parâmetros
    consultas = execute_query(query, tuple(params) if params else None)
    df = pd.DataFrame(consultas) if consultas else pd.DataFrame()
    
    if df.empty:
        return dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "Nenhuma consulta encontrada com os filtros selecionados."
        ], color="info")
    
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        page_size=15,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    )

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
    Output("consulta-edit-results", "children"),
    Input("btn-search-consulta", "n_clicks"),
    [State("consulta-edit-codcli", "value"),
     State("consulta-edit-codmed", "value"),
     State("consulta-edit-cpfpac", "value"),
     State("consulta-edit-datahora-antiga", "value")],
    prevent_initial_call=True
)
def search_consulta_list(n_clicks, cod_cli, cod_med, cpf_pac, data_hora_antiga):
    if not n_clicks:
        return ""
    
    # Check if at least one field is filled
    if not any([cod_cli, cod_med, cpf_pac, data_hora_antiga]):
        return dbc.Alert("Preencha pelo menos um campo para buscar.", color="warning")
    
    # Build dynamic query based on filled fields
    query_parts = []
    params = []
    
    if cod_cli:
        query_parts.append("c.CodCli = %s")
        params.append(cod_cli)
    if cod_med:
        query_parts.append("c.CodMed = %s")
        params.append(cod_med)
    if cpf_pac:
        query_parts.append("c.CpfPaciente = %s")
        params.append(cpf_pac)
    if data_hora_antiga:
        query_parts.append("c.Data_Hora = %s")
        params.append(data_hora_antiga)
    
    where_clause = " AND ".join(query_parts)
    
    query = f"""SELECT c.*, cli.NomeCli as Clinica_Nome, m.NomeMed as Medico_Nome, p.NomePac as Paciente_Nome
                FROM Consulta c
                JOIN Clinica cli ON c.CodCli = cli.CodCli
                JOIN Medico m ON c.CodMed = m.CodMed
                JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
                WHERE {where_clause}
                ORDER BY c.Data_Hora"""
    
    result = execute_query(query, tuple(params))
    
    if not result:
        return dbc.Alert("Nenhuma consulta encontrada com os critérios informados.", color="warning")
    
    # Create radio options for selection
    options = []
    for c in result:
        data_hora_str = str(c['Data_Hora'])
        label = f"{c['Clinica_Nome']} | {c['Medico_Nome']} | {c['Paciente_Nome']} | {data_hora_str}"
        value = f"{c['CodCli']}|{c['CodMed']}|{c['CpfPaciente']}|{data_hora_str}"
        options.append({'label': label, 'value': value})
    
    return html.Div([
        dbc.Alert(f"Encontradas {len(result)} consulta(s). Selecione uma para editar:", color="info"),
        dcc.RadioItems(
            id='consulta-edit-selector',
            options=options,
            labelStyle={'display': 'block', 'marginBottom': '10px'}
        )
    ])

@app.callback(
    [Output("consulta-edit-data", "value"),
     Output("consulta-edit-hora", "value"),
     Output("consulta-edit-data", "disabled"),
     Output("consulta-edit-hora", "disabled"),
     Output("btn-update-consulta", "disabled"),
     Output("msg-edit-consulta", "children"),
     Output("consulta-edit-selected-data", "data")],
    Input("consulta-edit-selector", "value"),
    prevent_initial_call=True
)
def select_consulta_for_edit(selected_value):
    if not selected_value:
        return "", "", True, True, True, "", None
    
    # Parse the selected value
    parts = selected_value.split('|')
    cod_cli, cod_med, cpf_pac, data_hora_antiga = parts
    
    # Fetch the specific consultation
    query = """SELECT * FROM Consulta 
               WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s AND Data_Hora = %s"""
    result = execute_query(query, (cod_cli, cod_med, cpf_pac, data_hora_antiga))
    
    if result:
        c = result[0]
        data_hora_str = str(c['Data_Hora'])
        data = data_hora_str.split(' ')[0]
        hora = data_hora_str.split(' ')[1][:5]
        
        # Store the original data
        stored_data = {
            'CodCli': cod_cli,
            'CodMed': cod_med,
            'CpfPaciente': cpf_pac,
            'Data_Hora': data_hora_antiga
        }
        
        return (data, hora, False, False, False,
               dbc.Alert("Consulta selecionada! Altere a data/hora desejada.", color="success"),
               stored_data)
    
    return "", "", True, True, True, dbc.Alert("Erro ao carregar consulta.", color="danger"), None

@app.callback(
    [Output("msg-edit-consulta", "children", allow_duplicate=True),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-update-consulta", "n_clicks"),
    [State("consulta-edit-selected-data", "data"),
     State("consulta-edit-data", "value"),
     State("consulta-edit-hora", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def update_consulta(n_clicks, selected_data, nova_data, nova_hora, current_refresh):
    if n_clicks and selected_data and nova_data and nova_hora:
        nova_data_hora = f"{nova_data} {nova_hora}:00"
        query = "UPDATE Consulta SET Data_Hora = %s WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s AND Data_Hora = %s"
        if execute_update(query, (nova_data_hora, selected_data['CodCli'], selected_data['CodMed'], 
                                  selected_data['CpfPaciente'], selected_data['Data_Hora'])):
            return dbc.Alert("Consulta atualizada com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao atualizar consulta!", color="danger"), current_refresh
    return "", current_refresh

@app.callback(
    Output("consulta-delete-results", "children"),
    Input("btn-search-delete-consulta", "n_clicks"),
    [State("consulta-delete-codcli", "value"),
     State("consulta-delete-codmed", "value"),
     State("consulta-delete-cpfpac", "value"),
     State("consulta-delete-datahora", "value")],
    prevent_initial_call=True
)
def search_delete_consulta_list(n_clicks, cod_cli, cod_med, cpf_pac, data_hora):
    if not n_clicks:
        return ""
    
    # Check if at least one field is filled
    if not any([cod_cli, cod_med, cpf_pac, data_hora]):
        return dbc.Alert("Preencha pelo menos um campo para buscar.", color="warning")
    
    # Build dynamic query based on filled fields
    query_parts = []
    params = []
    
    if cod_cli:
        query_parts.append("c.CodCli = %s")
        params.append(cod_cli)
    if cod_med:
        query_parts.append("c.CodMed = %s")
        params.append(cod_med)
    if cpf_pac:
        query_parts.append("c.CpfPaciente = %s")
        params.append(cpf_pac)
    if data_hora:
        query_parts.append("c.Data_Hora = %s")
        params.append(data_hora)
    
    where_clause = " AND ".join(query_parts)
    
    query = f"""SELECT c.*, cl.NomeCli, m.NomeMed, p.NomePac
                FROM Consulta c
                JOIN Clinica cl ON c.CodCli = cl.CodCli
                JOIN Medico m ON c.CodMed = m.CodMed
                JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
                WHERE {where_clause}
                ORDER BY c.Data_Hora"""
    
    result = execute_query(query, tuple(params))
    
    if not result:
        return dbc.Alert("Nenhuma consulta encontrada com os critérios informados.", color="warning")
    
    # Create radio options for selection
    options = []
    for c in result:
        data_hora_str = str(c['Data_Hora'])
        label = f"{c['NomeCli']} | {c['NomeMed']} | {c['NomePac']} | {data_hora_str}"
        value = f"{c['CodCli']}|{c['CodMed']}|{c['CpfPaciente']}|{data_hora_str}"
        options.append({'label': label, 'value': value})
    
    return html.Div([
        dbc.Alert(f"Encontradas {len(result)} consulta(s). Selecione uma para excluir:", color="info"),
        dcc.RadioItems(
            id='consulta-delete-selector',
            options=options,
            labelStyle={'display': 'block', 'marginBottom': '10px'}
        )
    ])

@app.callback(
    [Output("consulta-delete-info", "children"),
     Output("btn-delete-consulta", "disabled"),
     Output("consulta-delete-selected-data", "data")],
    Input("consulta-delete-selector", "value"),
    prevent_initial_call=True
)
def select_consulta_for_delete(selected_value):
    if not selected_value:
        return dbc.Alert("Digite a chave primária completa e clique em Buscar.", color="info"), True, None
    
    # Parse the selected value
    parts = selected_value.split('|')
    cod_cli, cod_med, cpf_pac, data_hora = parts
    
    # Fetch the specific consultation
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
        
        # Store the selected data
        stored_data = {
            'CodCli': cod_cli,
            'CodMed': cod_med,
            'CpfPaciente': cpf_pac,
            'Data_Hora': data_hora
        }
        
        return info, False, stored_data
    
    return dbc.Alert("Erro ao carregar consulta.", color="danger"), True, None

@app.callback(
    [Output("msg-delete-consulta", "children"),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-delete-consulta", "n_clicks"),
    [State("consulta-delete-selected-data", "data"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def delete_consulta(n_clicks, selected_data, current_refresh):
    if n_clicks and selected_data:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Primeiro deleta a consulta
            query = "DELETE FROM Consulta WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s AND Data_Hora = %s"
            cursor.execute(query, (selected_data['CodCli'], selected_data['CodMed'], 
                                   selected_data['CpfPaciente'], selected_data['Data_Hora']))
            
            # Depois chama o procedimento para promover da lista de espera
            cursor.callproc('sp_promover_lista_espera', [
                selected_data['CodCli'],
                selected_data['CodMed'],
                selected_data['Data_Hora'],
                selected_data['CpfPaciente']
            ])
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return dbc.Alert("Consulta excluída com sucesso! Verificando lista de espera...", color="success"), current_refresh + 1
        except Error as e:
            return dbc.Alert(f"Erro ao excluir consulta: {str(e)}", color="danger"), current_refresh
    return "", current_refresh

# ==================== LISTA DE ESPERA ====================
def render_lista_espera():
    # Buscar dados da lista de espera com tempo de espera calculado
    lista_espera = execute_query("""
        SELECT 
            le.IdEspera,
            c.NomeCli AS Clinica,
            m.NomeMed AS Medico,
            m.Especialidade,
            p.NomePac AS Paciente,
            DATE_FORMAT(le.DataHoraDesejada, '%d/%m/%Y %H:%i') as DataHoraDesejada,
            le.Prioridade,
            le.Status,
            DATE_FORMAT(le.DataHoraCadastro, '%d/%m/%Y %H:%i') as DataHoraCadastro,
            TIMESTAMPDIFF(DAY, le.DataHoraCadastro, NOW()) as DiasEspera,
            le.CodCli,
            le.CodMed,
            le.CpfPaciente
        FROM ListaEspera le
        JOIN Clinica c ON le.CodCli = c.CodCli
        JOIN Medico m ON le.CodMed = m.CodMed
        JOIN Paciente p ON le.CpfPaciente = p.CpfPaciente
        WHERE le.Status = 'aguardando'
        ORDER BY le.DataHoraDesejada, le.Prioridade DESC, le.DataHoraCadastro
    """)
    
    # Buscar histórico de promoções
    historico = execute_query("""
        SELECT 
            log.IdLog,
            c.NomeCli AS Clinica,
            m.NomeMed AS Medico,
            p.NomePac AS Paciente,
            log.DataHoraConsulta,
            log.DataHoraPromocao,
            log.Mensagem
        FROM LogListaEspera log
        JOIN Clinica c ON log.CodCli = c.CodCli
        JOIN Medico m ON log.CodMed = m.CodMed
        JOIN Paciente p ON log.CpfPaciente = p.CpfPaciente
        ORDER BY log.DataHoraPromocao DESC
        LIMIT 50
    """)
    
    df_espera = pd.DataFrame(lista_espera) if lista_espera else pd.DataFrame()
    df_historico = pd.DataFrame(historico) if historico else pd.DataFrame()
    
    # Buscar dados para dropdowns
    clinicas = execute_query("SELECT CodCli, NomeCli FROM Clinica")
    medicos = execute_query("SELECT CodMed, NomeMed, Especialidade FROM Medico")
    pacientes = execute_query("SELECT CpfPaciente, NomePac FROM Paciente")
    
    # Buscar especialidades para filtro
    especialidades = execute_query("SELECT DISTINCT Especialidade FROM Medico ORDER BY Especialidade")
    
    # Preparar colunas para exibição (incluindo ID da lista de espera)
    colunas_exibir = ['IdEspera', 'Clinica', 'Medico', 'Especialidade', 'Paciente', 'DataHoraDesejada', 'Prioridade', 'Status', 'DataHoraCadastro', 'DiasEspera']
    df_exibir = df_espera[colunas_exibir] if not df_espera.empty else pd.DataFrame()
    
    return html.Div([
        html.H3([
            html.I(className="fas fa-clock me-3", style={'color': '#0ea5e9'}),
            "Gestão de Lista de Espera"
        ], className="mb-4"),
        
        dbc.Tabs(active_tab="tab-listar-espera", children=[
            # Aba Listar
            dbc.Tab(label="Aguardando", tab_id="tab-listar-espera", children=[
                html.Div([
                    dbc.Alert([
                        html.I(className="fas fa-info-circle me-2"),
                        "Pacientes em ordem de prioridade e data de cadastro. Quando uma consulta for cancelada, o próximo da fila será automaticamente agendado."
                    ], color="info", className="mt-3"),
                    
                    # Filtros Avançados
                    dbc.Card([
                        dbc.CardBody([
                            html.H5([html.I(className="fas fa-filter me-2"), "Filtros de Pesquisa"], className="mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Especialidade"),
                                    dcc.Dropdown(
                                        id="filtro-espera-especialidade",
                                        options=[{'label': 'Todas', 'value': 'all'}] + 
                                                [{'label': e['Especialidade'], 'value': e['Especialidade']} for e in especialidades] if especialidades else [],
                                        value='all',
                                        clearable=False
                                    )
                                ], md=3),
                                dbc.Col([
                                    dbc.Label("Prioridade Mínima"),
                                    dcc.Dropdown(
                                        id="filtro-espera-prioridade",
                                        options=[
                                            {'label': 'Todas', 'value': 0},
                                            {'label': 'Média (1+)', 'value': 1},
                                            {'label': 'Alta (2+)', 'value': 2},
                                            {'label': 'Urgente (3+)', 'value': 3}
                                        ],
                                        value=0,
                                        clearable=False
                                    )
                                ], md=2),
                                dbc.Col([
                                    dbc.Label("Data Desejada - Início"),
                                    dbc.Input(id="filtro-espera-data-inicio", type="date")
                                ], md=2),
                                dbc.Col([
                                    dbc.Label("Data Desejada - Fim"),
                                    dbc.Input(id="filtro-espera-data-fim", type="date")
                                ], md=2),
                                dbc.Col([
                                    dbc.Label("Ordenar por"),
                                    dcc.Dropdown(
                                        id="filtro-espera-ordenacao",
                                        options=[
                                            {'label': 'Mais Dias Esperando', 'value': 'dias_desc'},
                                            {'label': 'Maior Prioridade', 'value': 'prioridade_desc'},
                                            {'label': 'Data Desejada', 'value': 'data_desejada'}
                                        ],
                                        value='prioridade_desc',
                                        clearable=False
                                    )
                                ], md=2),
                                dbc.Col([
                                    dbc.Label(html.Br()),
                                    dbc.Button([html.I(className="fas fa-search me-2"), "Filtrar"], 
                                              id="btn-filtrar-espera", color="warning", className="w-100")
                                ], md=1),
                            ])
                        ])
                    ], className="mb-3"),
                    
                    # Tabela de Resultados
                    html.Div(id="espera-filtrada-container", children=[
                        dash_table.DataTable(
                            id='table-lista-espera',
                            columns=[{"name": i, "id": i} for i in colunas_exibir],
                            data=df_exibir.to_dict('records') if not df_exibir.empty else [],
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'padding': '10px'},
                            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                            page_size=15,
                            style_data_conditional=[
                                {
                                    'if': {'filter_query': '{Prioridade} >= 3'},
                                    'backgroundColor': '#fee2e2',
                                    'fontWeight': 'bold'
                                },
                                {
                                    'if': {'filter_query': '{Prioridade} = 2'},
                                    'backgroundColor': '#fef3c7',
                                    'fontWeight': 'bold'
                                }
                            ]
                        )
                    ])
                ], className="mt-3")
            ]),
            
            # Aba Adicionar à Lista
            dbc.Tab(label="Adicionar à Espera", tab_id="tab-adicionar-espera", children=[
                dbc.Form([
                    dbc.Alert([
                        html.I(className="fas fa-lightbulb me-2"),
                        html.Strong("Prioridade: "),
                        "0 = Normal, 1 = Média, 2 = Alta, 3+ = Urgente"
                    ], color="warning", className="mt-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Clínica"),
                            dcc.Dropdown(
                                id="espera-clinica",
                                options=[{'label': c['NomeCli'], 'value': c['CodCli']} for c in clinicas] if clinicas else []
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Médico"),
                            dcc.Dropdown(
                                id="espera-medico",
                                options=[{'label': f"{m['NomeMed']} ({m['Especialidade']})", 'value': m['CodMed']} for m in medicos] if medicos else []
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Paciente"),
                            dcc.Dropdown(
                                id="espera-paciente",
                                options=[{'label': p['NomePac'], 'value': p['CpfPaciente']} for p in pacientes] if pacientes else []
                            )
                        ], width=4),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Data Desejada"),
                            dbc.Input(id="espera-data", type="date")
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Hora Desejada"),
                            dbc.Input(id="espera-hora", type="time")
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Prioridade (0-5)"),
                            dbc.Input(id="espera-prioridade", type="number", value=0, min=0, max=5)
                        ], width=4),
                    ], className="mt-3"),
                    dbc.Button("Adicionar à Lista de Espera", id="btn-add-espera", color="primary", className="mt-3"),
                    html.Div(id="msg-espera", className="mt-3")
                ], className="mt-3")
            ]),
            
            # Aba Cancelar da Lista
            dbc.Tab(label="Cancelar Espera", tab_id="tab-cancelar-espera", children=[
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("ID da Espera"),
                            dbc.Input(id="espera-delete-id", type="number", placeholder="Digite o ID")
                        ], width=6),
                        dbc.Col([
                            dbc.Button("Buscar", id="btn-search-delete-espera", color="info", className="mt-4")
                        ], width=2),
                    ]),
                    html.Hr(className="mt-3"),
                    html.Div(id="espera-delete-info", children=[
                        dbc.Alert("Digite um ID e clique em Buscar para visualizar os dados.", color="info")
                    ]),
                    dbc.Button("Confirmar Cancelamento", id="btn-delete-espera", color="danger", className="mt-3", disabled=True),
                    html.Div(id="msg-delete-espera", className="mt-3")
                ], className="mt-3")
            ]),
            
            # Aba Histórico
            dbc.Tab(label="Histórico de Promoções", tab_id="tab-historico-espera", children=[
                html.Div([
                    dbc.Alert([
                        html.I(className="fas fa-history me-2"),
                        "Histórico de pacientes que foram promovidos da lista de espera automaticamente pelo trigger."
                    ], color="success", className="mt-3"),
                    dash_table.DataTable(
                        id='table-historico-espera',
                        columns=[{"name": i, "id": i} for i in df_historico.columns] if not df_historico.empty else [],
                        data=df_historico.to_dict('records') if not df_historico.empty else [],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                    )
                ], className="mt-3")
            ]),
        ])
    ])

# Callback: Filtrar Lista de Espera
@app.callback(
    Output("espera-filtrada-container", "children"),
    [Input("btn-filtrar-espera", "n_clicks"),
     Input("refresh-trigger", "data")],
    [State("filtro-espera-especialidade", "value"),
     State("filtro-espera-prioridade", "value"),
     State("filtro-espera-data-inicio", "value"),
     State("filtro-espera-data-fim", "value"),
     State("filtro-espera-ordenacao", "value")],
    prevent_initial_call=False
)
def filtrar_lista_espera(n_clicks, refresh, especialidade, prioridade, data_inicio, data_fim, ordenacao):
    # Query com TIMESTAMPDIFF para calcular dias de espera + múltiplos JOINs
    query = """
        SELECT 
            le.IdEspera,
            c.NomeCli as Clinica,
            m.NomeMed as Medico,
            m.Especialidade,
            p.NomePac as Paciente,
            DATE_FORMAT(le.DataHoraDesejada, '%d/%m/%Y %H:%i') as DataHoraDesejada,
            le.Prioridade,
            le.Status,
            DATE_FORMAT(le.DataHoraCadastro, '%d/%m/%Y %H:%i') as DataHoraCadastro,
            TIMESTAMPDIFF(DAY, le.DataHoraCadastro, NOW()) as DiasEspera
        FROM ListaEspera le
        JOIN Clinica c ON le.CodCli = c.CodCli
        JOIN Medico m ON le.CodMed = m.CodMed
        JOIN Paciente p ON le.CpfPaciente = p.CpfPaciente
        WHERE le.Status = 'aguardando'
    """
    params = []
    
    # Filtro: Especialidade
    if especialidade and especialidade != 'all':
        query += " AND m.Especialidade = %s"
        params.append(especialidade)
    
    # Filtro: Prioridade Mínima
    if prioridade and int(prioridade) > 0:
        query += " AND le.Prioridade >= %s"
        params.append(int(prioridade))
    
    # Filtro: Período Desejado (Data Inicial e Final)
    if data_inicio:
        query += " AND DATE(le.DataHoraDesejada) >= %s"
        params.append(data_inicio)
    
    if data_fim:
        query += " AND DATE(le.DataHoraDesejada) <= %s"
        params.append(data_fim)
    
    # Ordenação Dinâmica
    if ordenacao == 'dias_desc':
        query += " ORDER BY DiasEspera DESC, le.Prioridade DESC"
    elif ordenacao == 'prioridade_desc':
        query += " ORDER BY le.Prioridade DESC, DiasEspera DESC"
    elif ordenacao == 'data_desejada':
        query += " ORDER BY le.DataHoraDesejada ASC, le.Prioridade DESC"
    else:
        query += " ORDER BY le.Prioridade DESC, le.DataHoraCadastro ASC"
    
    espera = execute_query(query, tuple(params) if params else None)
    df = pd.DataFrame(espera) if espera else pd.DataFrame()
    
    if df.empty:
        return dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "Nenhum paciente na lista de espera com os filtros selecionados."
        ], color="info")
    
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        page_size=15,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {'filter_query': '{Prioridade} >= 3'},
                'backgroundColor': '#fee2e2',
                'fontWeight': 'bold',
                'color': '#991b1b'
            },
            {
                'if': {'filter_query': '{Prioridade} = 2'},
                'backgroundColor': '#fef3c7',
                'fontWeight': 'bold',
                'color': '#92400e'
            },
            {
                'if': {'filter_query': '{DiasEspera} >= 30'},
                'backgroundColor': '#dbeafe',
                'color': '#1e40af'
            }
        ]
    )

# Callback: Adicionar à Lista de Espera
@app.callback(
    [Output("msg-espera", "children"),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-add-espera", "n_clicks"),
    [State("espera-clinica", "value"),
     State("espera-medico", "value"),
     State("espera-paciente", "value"),
     State("espera-data", "value"),
     State("espera-hora", "value"),
     State("espera-prioridade", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def add_lista_espera(n_clicks, cod_cli, cod_med, cpf_pac, data, hora, prioridade, current_refresh):
    if n_clicks and cod_cli and cod_med and cpf_pac and data and hora:
        data_hora = f"{data} {hora}:00"
        query = "INSERT INTO ListaEspera (CodCli, CodMed, CpfPaciente, DataHoraDesejada, Prioridade) VALUES (%s, %s, %s, %s, %s)"
        if execute_update(query, (cod_cli, cod_med, cpf_pac, data_hora, prioridade or 0)):
            return dbc.Alert("Paciente adicionado à lista de espera com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao adicionar à lista de espera!", color="danger"), current_refresh
    return "", current_refresh

# Callback: Buscar para Cancelar
@app.callback(
    [Output("espera-delete-info", "children"),
     Output("btn-delete-espera", "disabled")],
    Input("btn-search-delete-espera", "n_clicks"),
    State("espera-delete-id", "value"),
    prevent_initial_call=True
)
def search_delete_espera(n_clicks, id_espera):
    if n_clicks and id_espera:
        result = execute_query("""
            SELECT 
                le.IdEspera,
                c.NomeCli AS Clinica,
                m.NomeMed AS Medico,
                m.Especialidade,
                p.NomePac AS Paciente,
                le.DataHoraDesejada,
                le.Prioridade,
                le.Status
            FROM ListaEspera le
            JOIN Clinica c ON le.CodCli = c.CodCli
            JOIN Medico m ON le.CodMed = m.CodMed
            JOIN Paciente p ON le.CpfPaciente = p.CpfPaciente
            WHERE le.IdEspera = %s
        """, (id_espera,))
        if result:
            e = result[0]
            info = dbc.Card([
                dbc.CardHeader("Dados da Lista de Espera a ser Cancelada", className="bg-danger text-white"),
                dbc.CardBody([
                    html.P([html.Strong("ID: "), str(e['IdEspera'])]),
                    html.P([html.Strong("Clínica: "), e['Clinica']]),
                    html.P([html.Strong("Médico: "), f"{e['Medico']} ({e['Especialidade']})"])    ,
                    html.P([html.Strong("Paciente: "), e['Paciente']]),
                    html.P([html.Strong("Data/Hora Desejada: "), str(e['DataHoraDesejada'])]),
                    html.P([html.Strong("Prioridade: "), str(e['Prioridade'])]),
                    html.P([html.Strong("Status: "), e['Status']]),
                ])
            ])
            return info, False
        return dbc.Alert(f"Registro {id_espera} não encontrado!", color="danger"), True
    return dbc.Alert("Digite um ID e clique em Buscar.", color="info"), True

# Callback: Confirmar Cancelamento
@app.callback(
    [Output("msg-delete-espera", "children"),
     Output("refresh-trigger", "data", allow_duplicate=True)],
    Input("btn-delete-espera", "n_clicks"),
    [State("espera-delete-id", "value"),
     State("refresh-trigger", "data")],
    prevent_initial_call=True
)
def delete_espera(n_clicks, id_espera, current_refresh):
    if n_clicks and id_espera:
        query = "UPDATE ListaEspera SET Status = 'cancelado' WHERE IdEspera = %s"
        if execute_update(query, (id_espera,)):
            return dbc.Alert("Espera cancelada com sucesso!", color="success"), current_refresh + 1
        return dbc.Alert("Erro ao cancelar espera!", color="danger"), current_refresh
    return "", current_refresh

# ==================== GRÁFICOS ====================
def render_graficos():
    return html.Div([
        html.H3([
            html.I(className="fas fa-chart-pie me-3", style={'color': '#0ea5e9'}),
            "Visualizações e Análises"
        ], className="mb-4"),
        
        dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "Análises visuais e estatísticas do sistema de gestão clínica."
        ], color="info", className="mb-4"),
        
        # Linha 1: Consultas por Especialidade + Lista de Espera vs Consultas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Consultas por Especialidade", className="text-center mb-3"),
                        dcc.Graph(id='graph-especialidade')
                    ])
                ], className="shadow-sm")
            ], lg=6, md=12, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Lista de Espera vs Consultas Agendadas", className="text-center mb-3"),
                        dcc.Graph(id='graph-lista-espera')
                    ])
                ], className="shadow-sm")
            ], lg=6, md=12, className="mb-4"),
        ]),
        
        # Linha 2: Consultas por Clínica + Crescimento de Consultas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Consultas por Clínica", className="text-center mb-3"),
                        dcc.Graph(id='graph-clinica')
                    ])
                ], className="shadow-sm")
            ], lg=6, md=12, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Crescimento de Consultas (Últimos 6 Meses)", className="text-center mb-3"),
                        dcc.Graph(id='graph-crescimento')
                    ])
                ], className="shadow-sm")
            ], lg=6, md=12, className="mb-4"),
        ]),
        
        # Linha 3: Top 10 Médicos + Distribuição de Gênero (Médicos e Pacientes)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Top 10 Médicos Mais Procurados", className="text-center mb-3"),
                        dcc.Graph(id='graph-top-medicos')
                    ])
                ], className="shadow-sm")
            ], lg=6, md=12, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Distribuição de Gênero - Médicos", className="text-center mb-3"),
                        dcc.Graph(id='graph-genero-medicos')
                    ])
                ], className="shadow-sm")
            ], lg=3, md=6, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Distribuição de Gênero - Pacientes", className="text-center mb-3"),
                        dcc.Graph(id='graph-genero-pacientes')
                    ])
                ], className="shadow-sm")
            ], lg=3, md=6, className="mb-4"),
        ]),
        
        # Seção de Consultas Avançadas
        html.Hr(className="my-4"),
        dbc.Row([
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-chart-line me-2"),
                    "Consultas Avançadas"
                ], className="text-primary mb-3")
            ])
        ]),
        
        # Linha 1 de Consultas Avançadas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Pacientes por Faixa Etária", className="text-center mb-3"),
                        dcc.Graph(id='graph-faixa-etaria')
                    ])
                ], className="shadow-sm")
            ], lg=6, md=12, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Pacientes com Múltiplas Consultas", className="text-center mb-3"),
                        dcc.Graph(id='graph-pacientes-frequentes')
                    ])
                ], className="shadow-sm")
            ], lg=6, md=12, className="mb-4"),
        ]),
        
        # Linha 2 de Consultas Avançadas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Taxa de Ocupação por Clínica", className="text-center mb-3"),
                        dcc.Graph(id='graph-taxa-ocupacao')
                    ])
                ], className="shadow-sm")
            ], lg=6, md=12, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Horários de Pico de Consultas", className="text-center mb-3"),
                        dcc.Graph(id='graph-horarios-pico')
                    ])
                ], className="shadow-sm")
            ], lg=6, md=12, className="mb-4"),
        ]),
        
        dcc.Interval(id='interval-graficos', interval=30000, n_intervals=0)
    ])

@app.callback(
    [Output('graph-especialidade', 'figure'),
     Output('graph-lista-espera', 'figure'),
     Output('graph-clinica', 'figure'),
     Output('graph-crescimento', 'figure'),
     Output('graph-top-medicos', 'figure'),
     Output('graph-genero-medicos', 'figure'),
     Output('graph-genero-pacientes', 'figure'),
     Output('graph-faixa-etaria', 'figure'),
     Output('graph-pacientes-frequentes', 'figure'),
     Output('graph-taxa-ocupacao', 'figure'),
     Output('graph-horarios-pico', 'figure')],
    [Input('interval-graficos', 'n_intervals'),
     Input('refresh-trigger', 'data')]
)
def update_graficos(n, refresh):
    # 1. Consultas por Especialidade
    data_especialidade = execute_query("""
        SELECT m.Especialidade, COUNT(*) as Total
        FROM Consulta c
        JOIN Medico m ON c.CodMed = m.CodMed
        GROUP BY m.Especialidade
        ORDER BY Total DESC
    """)
    
    if data_especialidade:
        df_esp = pd.DataFrame(data_especialidade)
        fig_esp = px.pie(df_esp, names='Especialidade', values='Total', 
                         hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
        fig_esp.update_traces(textposition='inside', textinfo='percent+label')
        fig_esp.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    else:
        fig_esp = go.Figure()
        fig_esp.add_annotation(text="Sem dados", showarrow=False)
    
    # 2. Lista de Espera vs Consultas Agendadas
    data_lista = execute_query("""
        SELECT m.Especialidade,
               COUNT(DISTINCT c.CodMed, c.CpfPaciente, c.Data_Hora) as Consultas,
               COUNT(DISTINCT le.IdEspera) as ListaEspera
        FROM Medico m
        LEFT JOIN Consulta c ON m.CodMed = c.CodMed
        LEFT JOIN ListaEspera le ON m.CodMed = le.CodMed AND le.Status = 'aguardando'
        GROUP BY m.Especialidade
        ORDER BY Consultas DESC
    """)
    
    if data_lista:
        df_lista = pd.DataFrame(data_lista)
        fig_lista = go.Figure()
        fig_lista.add_trace(go.Bar(
            name='Consultas Agendadas',
            x=df_lista['Especialidade'],
            y=df_lista['Consultas'],
            marker_color='#3b82f6'
        ))
        fig_lista.add_trace(go.Bar(
            name='Lista de Espera',
            x=df_lista['Especialidade'],
            y=df_lista['ListaEspera'],
            marker_color='#f59e0b'
        ))
        fig_lista.update_layout(barmode='stack', xaxis_title='', yaxis_title='Quantidade',
                               legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                               margin=dict(t=30, b=0, l=0, r=0))
    else:
        fig_lista = go.Figure()
        fig_lista.add_annotation(text="Sem dados", showarrow=False)
    
    # 3. Consultas por Clínica
    data_clinica = execute_query("""
        SELECT cl.NomeCli as Clinica, COUNT(*) as Total
        FROM Consulta c
        JOIN Clinica cl ON c.CodCli = cl.CodCli
        GROUP BY cl.NomeCli
        ORDER BY Total DESC
    """)
    
    if data_clinica:
        df_cli = pd.DataFrame(data_clinica)
        fig_cli = px.bar(df_cli, x='Clinica', y='Total', color_discrete_sequence=['#10b981'])
        fig_cli.update_layout(xaxis_title='', yaxis_title='Consultas', showlegend=False,
                             margin=dict(t=0, b=0, l=0, r=0))
        fig_cli.update_traces(text=df_cli['Total'], textposition='outside')
    else:
        fig_cli = go.Figure()
        fig_cli.add_annotation(text="Sem dados", showarrow=False)
    
    # 4. Crescimento de Consultas (Últimos 6 meses)
    data_crescimento = execute_query("""
        SELECT DATE_FORMAT(Data_Hora, '%Y-%m') as Mes, COUNT(*) as Total
        FROM Consulta
        WHERE Data_Hora >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY Mes
        ORDER BY Mes
    """)
    
    if data_crescimento:
        df_cresc = pd.DataFrame(data_crescimento)
        fig_cresc = px.area(df_cresc, x='Mes', y='Total', color_discrete_sequence=['#8b5cf6'])
        fig_cresc.update_layout(xaxis_title='Mês', yaxis_title='Consultas',
                               margin=dict(t=0, b=0, l=0, r=0))
        fig_cresc.update_traces(hovertemplate='Mês: %{x}<br>Consultas: %{y}<extra></extra>')
    else:
        fig_cresc = go.Figure()
        fig_cresc.add_annotation(text="Sem dados", showarrow=False)
    
    # 5. Top 10 Médicos Mais Procurados
    data_top_medicos = execute_query("""
        SELECT m.NomeMed as Medico, m.Especialidade, COUNT(*) as Total
        FROM Consulta c
        JOIN Medico m ON c.CodMed = m.CodMed
        GROUP BY m.CodMed, m.NomeMed, m.Especialidade
        ORDER BY Total DESC
        LIMIT 10
    """)
    
    if data_top_medicos:
        df_top = pd.DataFrame(data_top_medicos)
        fig_top = px.bar(df_top, y='Medico', x='Total', orientation='h',
                        color_discrete_sequence=['#06b6d4'],
                        hover_data={'Total': True, 'Especialidade': True, 'Medico': False})
        fig_top.update_layout(yaxis_title='', xaxis_title='Consultas', showlegend=False,
                             margin=dict(t=0, b=0, l=0, r=0))
        fig_top.update_traces(text=df_top['Total'], textposition='outside', texttemplate='%{text:.0f}')
        fig_top.update_yaxes(categoryorder='total ascending')
        fig_top.update_xaxes(tickformat='d', dtick=1)
    else:
        fig_top = go.Figure()
        fig_top.add_annotation(text="Sem dados", showarrow=False)
    
    # 6. Distribuição de Gênero - Médicos
    data_genero_med = execute_query("""
        SELECT 
            CASE 
                WHEN Genero = 'M' THEN 'Masculino'
                WHEN Genero = 'F' THEN 'Feminino'
                WHEN Genero IS NULL OR Genero = '' THEN 'Não informado'
                ELSE Genero
            END as Genero,
            COUNT(*) as Total
        FROM Medico
        GROUP BY Genero
    """)
    
    if data_genero_med:
        df_gen_med = pd.DataFrame(data_genero_med)
        color_map = {'Masculino': '#10b981', 'Feminino': '#f59e0b', 'Não informado': '#94a3b8'}
        cores = [color_map.get(g, '#94a3b8') for g in df_gen_med['Genero']]
        
        fig_gen_med = go.Figure(data=[go.Pie(
            labels=df_gen_med['Genero'],
            values=df_gen_med['Total'],
            marker=dict(colors=cores),
            textinfo='percent+label',
            textposition='inside'
        )])
        fig_gen_med.update_layout(
            showlegend=True,
            legend=dict(orientation='h', yanchor='top', y=-0.1, xanchor='center', x=0.5),
            margin=dict(t=0, b=40, l=0, r=0)
        )
    else:
        fig_gen_med = go.Figure()
        fig_gen_med.add_annotation(text="Sem dados", showarrow=False)
    
    # 7. Distribuição de Gênero - Pacientes
    data_genero_pac = execute_query("""
        SELECT 
            CASE 
                WHEN Genero = 'M' THEN 'Masculino'
                WHEN Genero = 'F' THEN 'Feminino'
                WHEN Genero IS NULL OR Genero = '' THEN 'Não informado'
                ELSE Genero
            END as Genero,
            COUNT(*) as Total
        FROM Paciente
        GROUP BY Genero
    """)
    
    if data_genero_pac:
        df_gen_pac = pd.DataFrame(data_genero_pac)
        color_map = {'Masculino': '#10b981', 'Feminino': '#f59e0b', 'Não informado': '#94a3b8'}
        cores = [color_map.get(g, '#94a3b8') for g in df_gen_pac['Genero']]
        
        fig_gen_pac = go.Figure(data=[go.Pie(
            labels=df_gen_pac['Genero'],
            values=df_gen_pac['Total'],
            marker=dict(colors=cores),
            textinfo='percent+label',
            textposition='inside'
        )])
        fig_gen_pac.update_layout(
            showlegend=True,
            legend=dict(orientation='h', yanchor='top', y=-0.1, xanchor='center', x=0.5),
            margin=dict(t=0, b=40, l=0, r=0)
        )
    else:
        fig_gen_pac = go.Figure()
        fig_gen_pac.add_annotation(text="Sem dados", showarrow=False)
    
    # 8. Pacientes por Faixa Etária (usando TIMESTAMPDIFF)
    data_faixa_etaria = execute_query("""
        SELECT 
            CASE 
                WHEN TIMESTAMPDIFF(YEAR, DataNascimento, CURDATE()) < 18 THEN 'Criança/Adolescente (0-17)'
                WHEN TIMESTAMPDIFF(YEAR, DataNascimento, CURDATE()) BETWEEN 18 AND 35 THEN 'Jovem Adulto (18-35)'
                WHEN TIMESTAMPDIFF(YEAR, DataNascimento, CURDATE()) BETWEEN 36 AND 59 THEN 'Adulto (36-59)'
                ELSE 'Idoso (60+)'
            END as FaixaEtaria,
            COUNT(*) as Total
        FROM Paciente
        GROUP BY FaixaEtaria
        ORDER BY 
            CASE FaixaEtaria
                WHEN 'Criança/Adolescente (0-17)' THEN 1
                WHEN 'Jovem Adulto (18-35)' THEN 2
                WHEN 'Adulto (36-59)' THEN 3
                WHEN 'Idoso (60+)' THEN 4
            END
    """)
    
    if data_faixa_etaria:
        df_faixa = pd.DataFrame(data_faixa_etaria)
        fig_faixa = px.bar(df_faixa, x='FaixaEtaria', y='Total', 
                          color_discrete_sequence=['#8b5cf6'])
        fig_faixa.update_layout(xaxis_title='', yaxis_title='Pacientes', showlegend=False,
                               margin=dict(t=0, b=0, l=0, r=0))
        fig_faixa.update_traces(text=df_faixa['Total'], textposition='outside')
    else:
        fig_faixa = go.Figure()
        fig_faixa.add_annotation(text="Sem dados", showarrow=False)
    
    # 9. Pacientes com Múltiplas Consultas (usando COUNT + HAVING)
    data_pacientes_freq = execute_query("""
        SELECT 
            p.NomePac as Paciente,
            TIMESTAMPDIFF(YEAR, p.DataNascimento, CURDATE()) as Idade,
            COUNT(*) as TotalConsultas
        FROM Consulta c
        JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
        GROUP BY p.CpfPaciente, p.NomePac, p.DataNascimento
        HAVING COUNT(*) >= 2
        ORDER BY TotalConsultas DESC
        LIMIT 10
    """)
    
    if data_pacientes_freq:
        df_freq = pd.DataFrame(data_pacientes_freq)
        fig_freq = px.bar(df_freq, y='Paciente', x='TotalConsultas', orientation='h',
                         color='TotalConsultas', color_continuous_scale='Reds',
                         hover_data={'Idade': True, 'TotalConsultas': True, 'Paciente': False})
        fig_freq.update_layout(yaxis_title='', xaxis_title='Consultas', showlegend=False,
                              margin=dict(t=0, b=0, l=0, r=0))
        fig_freq.update_traces(text=df_freq['TotalConsultas'], textposition='outside')
        fig_freq.update_yaxes(categoryorder='total ascending')
        fig_freq.update_xaxes(tickformat='d', dtick=1)
    else:
        fig_freq = go.Figure()
        fig_freq.add_annotation(text="Sem pacientes com múltiplas consultas", showarrow=False)
    
    # 10. Taxa de Ocupação por Clínica (usando LEFT JOIN e COUNT)
    data_ocupacao = execute_query("""
        SELECT 
            cl.NomeCli as Clinica,
            COUNT(DISTINCT c.CodMed) as TotalMedicos,
            COUNT(c.CodMed) as TotalConsultas,
            ROUND(COUNT(c.CodMed) / GREATEST(COUNT(DISTINCT c.CodMed), 1), 2) as TaxaOcupacao
        FROM Clinica cl
        LEFT JOIN Consulta c ON cl.CodCli = c.CodCli
        GROUP BY cl.CodCli, cl.NomeCli
        ORDER BY TaxaOcupacao DESC
    """)
    
    if data_ocupacao:
        df_ocup = pd.DataFrame(data_ocupacao)
        fig_ocup = px.bar(df_ocup, x='Clinica', y='TaxaOcupacao',
                         color='TaxaOcupacao', color_continuous_scale='Viridis',
                         hover_data={'TotalMedicos': True, 'TotalConsultas': True})
        fig_ocup.update_layout(xaxis_title='', yaxis_title='Consultas/Médico', 
                              showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        fig_ocup.update_traces(text=[f'{x:.1f}' for x in df_ocup['TaxaOcupacao']], 
                              textposition='outside')
    else:
        fig_ocup = go.Figure()
        fig_ocup.add_annotation(text="Sem dados", showarrow=False)
    
    # 11. Horários de Pico de Consultas (usando DATE_FORMAT para extrair hora)
    data_horarios = execute_query("""
        SELECT 
            DATE_FORMAT(Data_Hora, '%H:00') as Horario,
            COUNT(*) as Total
        FROM Consulta
        GROUP BY Horario
        ORDER BY Horario
    """)
    
    if data_horarios:
        df_horarios = pd.DataFrame(data_horarios)
        fig_horarios = px.line(df_horarios, x='Horario', y='Total', 
                              markers=True, color_discrete_sequence=['#06b6d4'])
        fig_horarios.update_layout(xaxis_title='Horário', yaxis_title='Consultas',
                                  showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        fig_horarios.update_traces(line=dict(width=3))
    else:
        fig_horarios = go.Figure()
        fig_horarios.add_annotation(text="Sem dados", showarrow=False)
    
    return fig_esp, fig_lista, fig_cli, fig_cresc, fig_top, fig_gen_med, fig_gen_pac, fig_faixa, fig_freq, fig_ocup, fig_horarios

if __name__ == '__main__':
    app.run(debug=True)