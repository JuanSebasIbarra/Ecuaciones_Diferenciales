import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime

# Inicializar la app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Framework Analytics"

# Datos reales de frameworks con fechas de lanzamiento
frameworks_data = {
    'React': {
        'launch_date': '2013-05-29',
        'color': '#61DAFB',
        'npm_weekly': 25000000,
        'github_stars': 228000,
        'r': 0.65,
        'K': 1.0,
        'd': 0.08,
        'U0': 0.001
    },
    'Vue': {
        'launch_date': '2014-02-14',
        'color': '#42B883',
        'npm_weekly': 5200000,
        'github_stars': 207000,
        'r': 0.58,
        'K': 0.75,
        'd': 0.12,
        'U0': 0.001
    },
    'Angular': {
        'launch_date': '2016-09-14',
        'color': '#DD0031',
        'npm_weekly': 3800000,
        'github_stars': 95000,
        'r': 0.52,
        'K': 0.70,
        'd': 0.15,
        'U0': 0.05
    },
    'Svelte': {
        'launch_date': '2016-11-26',
        'color': '#FF3E00',
        'npm_weekly': 800000,
        'github_stars': 78000,
        'r': 0.72,
        'K': 0.45,
        'd': 0.07,
        'U0': 0.001
    },
    'Next.js': {
        'launch_date': '2016-10-25',
        'color': "#FFFFFF",
        'npm_weekly': 7500000,
        'github_stars': 124000,
        'r': 0.68,
        'K': 0.65,
        'd': 0.09,
        'U0': 0.001
    },
    'Nuxt': {
        'launch_date': '2016-10-16',
        'color': '#00DC82',
        'npm_weekly': 950000,
        'github_stars': 53000,
        'r': 0.55,
        'K': 0.40,
        'd': 0.11,
        'U0': 0.001
    }
}

def simulate_adoption(framework_name, data):
    """Simula la adopción usando el método de Euler desde la fecha de lanzamiento"""
    launch_date = datetime.strptime(data['launch_date'], '%Y-%m-%d')
    current_date = datetime.now()
    
    # Calcular años desde el lanzamiento
    years_elapsed = (current_date - launch_date).days / 365.25
    
    # Parámetros del modelo
    r = data['r']
    K = data['K']
    d = data['d']
    U0 = data['U0']
    
    # Simulación
    t_max = years_elapsed + 2  # Proyectar 2 años más
    dt = 0.01
    steps = int(t_max / dt)
    
    t = np.zeros(steps)
    U = np.zeros(steps)
    U[0] = U0
    
    dates = []
    
    for i in range(1, steps):
        t[i] = i * dt
        dUdt = r * U[i-1] * (1 - U[i-1] / K) - d * U[i-1]
        U[i] = max(0, U[i-1] + dUdt * dt)
        
        # Calcular fecha correspondiente
        days_from_launch = t[i] * 365.25
        date = launch_date + pd.Timedelta(days=days_from_launch)
        dates.append(date)
    
    return dates[1:], U[1:] * 100

# Generar datos de simulación para todos los frameworks
simulation_data = {}
for fw_name, fw_data in frameworks_data.items():
    dates, adoption = simulate_adoption(fw_name, fw_data)
    simulation_data[fw_name] = {
        'dates': dates,
        'adoption': adoption,
        'data': fw_data
    }

# Layout de la aplicación
app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1("Modelo de adopción de Frameworks", 
                   style={'margin': '0', 'color': 'white', 'fontSize': '32px'}),
            html.P("Análisis de crecimiento y adopción de frameworks JavaScript",
                  style={'margin': '5px 0 0 0', 'color': '#94a3b8', 'fontSize': '14px'})
        ], style={'flex': '1'}),
        
        html.Div([
            html.A([
                html.Img(
                    src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png',
                    style={
                        'height': '35px',
                        'width': '35px',
                        'marginRight': '20px',
                        'filter': 'invert(1)',
                        'cursor': 'pointer',
                        'transition': 'opacity 0.3s'
                    }
                )
            ], href='https://github.com/JuanSebasIbarra/Ecuaciones_Diferenciales.git', 
               target='_blank',
               style={'display': 'flex', 'alignItems': 'center'}),
            
            dcc.Dropdown(
                id='framework-selector',
                options=[{'label': name, 'value': name} for name in frameworks_data.keys()],
                value='React',
                style={
                    'width': '200px',
                    'backgroundColor': '#1e293b',
                    'color': 'white',
                    'border': '1px solid #334155'
                }
            )
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '20px'})
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'padding': '30px 40px',
        'backgroundColor': '#0f172a',
        'borderBottom': '1px solid #1e293b'
    }),
    
    # Stats Cards
    html.Div(id='stats-cards', style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
        'gap': '20px',
        'padding': '30px 40px',
        'backgroundColor': '#0f172a'
    }),
    
    # Main Chart
    html.Div([
        dcc.Graph(id='main-chart', style={'height': '500px'})
    ], style={
        'padding': '20px 40px',
        'backgroundColor': '#0f172a'
    }),
    
    # Comparison Section
    html.Div([
        html.H2("Comparación de Frameworks", 
               style={'color': 'white', 'fontSize': '24px', 'marginBottom': '20px'}),
        dcc.Graph(id='comparison-chart', style={'height': '500px'})
    ], style={
        'padding': '40px',
        'backgroundColor': '#0f172a',
        'borderTop': '1px solid #1e293b'
    })
    
], style={
    'backgroundColor': '#0f172a',
    'minHeight': '100vh',
    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
})

@app.callback(
    [Output('stats-cards', 'children'),
     Output('main-chart', 'figure')],
    [Input('framework-selector', 'value')]
)
def update_dashboard(selected_framework):
    if not selected_framework:
        selected_framework = 'React'
    
    fw_sim = simulation_data[selected_framework]
    fw_data = fw_sim['data']
    
    # Crear cards de estadísticas
    stats_cards = [
        # NPM Downloads
        html.Div([
            html.Div([
                html.Span("", style={'fontSize': '24px'}),
            ], style={'marginBottom': '10px'}),
            html.H3(f"{fw_data['npm_weekly']:,}", 
                   style={'color': 'white', 'margin': '0', 'fontSize': '28px', 'fontWeight': 'bold'}),
            html.P("NPM Downloads/week", 
                  style={'color': '#64748b', 'margin': '5px 0 0 0', 'fontSize': '14px'})
        ], style={
            'backgroundColor': '#1e293b',
            'padding': '25px',
            'borderRadius': '12px',
            'border': '1px solid #334155'
        }),
        
        # GitHub Stars
        html.Div([
            html.Div([
                html.Span("", style={'fontSize': '24px'}),
            ], style={'marginBottom': '10px'}),
            html.H3(f"{fw_data['github_stars']:,}", 
                   style={'color': 'white', 'margin': '0', 'fontSize': '28px', 'fontWeight': 'bold'}),
            html.P("GitHub Stars", 
                  style={'color': '#64748b', 'margin': '5px 0 0 0', 'fontSize': '14px'})
        ], style={
            'backgroundColor': '#1e293b',
            'padding': '25px',
            'borderRadius': '12px',
            'border': '1px solid #334155'
        }),
        
        # Tasa de Crecimiento
        html.Div([
            html.Div([
                html.Span("", style={'fontSize': '24px'}),
            ], style={'marginBottom': '10px'}),
            html.H3(f"{fw_data['r']:.2f}", 
                   style={'color': 'white', 'margin': '0', 'fontSize': '28px', 'fontWeight': 'bold'}),
            html.P("Tasa de Adopción", 
                  style={'color': '#64748b', 'margin': '5px 0 0 0', 'fontSize': '14px'})
        ], style={
            'backgroundColor': '#1e293b',
            'padding': '25px',
            'borderRadius': '12px',
            'border': '1px solid #334155'
        }),
        
        # Fecha de Lanzamiento
        html.Div([
            html.Div([
                html.Span("", style={'fontSize': '24px'}),
            ], style={'marginBottom': '10px'}),
            html.H3(fw_data['launch_date'], 
                   style={'color': 'white', 'margin': '0', 'fontSize': '22px', 'fontWeight': 'bold'}),
            html.P("Fecha de Lanzamiento", 
                  style={'color': '#64748b', 'margin': '5px 0 0 0', 'fontSize': '14px'})
        ], style={
            'backgroundColor': '#1e293b',
            'padding': '25px',
            'borderRadius': '12px',
            'border': '1px solid #334155'
        })
    ]
    
    # Crear gráfica principal
    fig = go.Figure()
    
    # Filtrar datos para mostrar solo desde la fecha de lanzamiento
    launch_date = datetime.strptime(fw_data['launch_date'], '%Y-%m-%d')
    filtered_dates = [d for d in fw_sim['dates'] if d >= launch_date]
    filtered_adoption = fw_sim['adoption'][-len(filtered_dates):]
    
    fig.add_trace(go.Scatter(
        x=filtered_dates,
        y=filtered_adoption,
        mode='lines',
        name=selected_framework,
        line=dict(color=fw_data['color'], width=3),
        fill='tozeroy',
        fillcolor=f"rgba({int(fw_data['color'][1:3], 16)}, {int(fw_data['color'][3:5], 16)}, {int(fw_data['color'][5:7], 16)}, 0.1)"
    ))
    
    fig.update_layout(
        title=dict(
            text=f"Curva de Adopción - {selected_framework}",
            font=dict(color='white', size=20),
            x=0
        ),
        xaxis=dict(
            title="Año",
            gridcolor='#1e293b',
            color='#94a3b8',
            showgrid=True,
            range=[launch_date, max(filtered_dates)]
        ),
        yaxis=dict(
            title="Adopción (%)",
            gridcolor='#1e293b',
            color='#94a3b8',
            showgrid=True
        ),
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        hovermode='x unified',
        margin=dict(l=60, r=40, t=60, b=60)
    )
    
    return stats_cards, fig

@app.callback(
    Output('comparison-chart', 'figure'),
    [Input('framework-selector', 'value')]
)
def update_comparison(selected_framework):
    fig = go.Figure()
    
    # Agregar todas las curvas filtrando desde su fecha de lanzamiento
    for fw_name, fw_sim in simulation_data.items():
        launch_date = datetime.strptime(fw_sim['data']['launch_date'], '%Y-%m-%d')
        filtered_dates = [d for d in fw_sim['dates'] if d >= launch_date]
        filtered_adoption = fw_sim['adoption'][-len(filtered_dates):]
        
        fig.add_trace(go.Scatter(
            x=filtered_dates,
            y=filtered_adoption,
            mode='lines',
            name=fw_name,
            line=dict(color=fw_sim['data']['color'], width=3)
        ))
    
    fig.update_layout(
        title=dict(
            text="Comparación de Todos los Frameworks",
            font=dict(color='white', size=20),
            x=0
        ),
        xaxis=dict(
            title="Año",
            gridcolor='#1e293b',
            color='#94a3b8',
            showgrid=True
        ),
        yaxis=dict(
            title="Adopción (%)",
            gridcolor='#1e293b',
            color='#94a3b8',
            showgrid=True
        ),
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        hovermode='x unified',
        legend=dict(
            font=dict(color='white'),
            bgcolor='#1e293b',
            bordercolor='#334155',
            borderwidth=1
        ),
        margin=dict(l=60, r=40, t=60, b=60)
    )
    
    return fig

if __name__ == '__main__':
    print("\n Modelo de adopción de Frameworks")
    print(" El puerto a usar: http://127.0.0.1:8050\n")
    app.run(debug=True, port=8050)