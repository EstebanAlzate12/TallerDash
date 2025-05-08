import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Cargar los datos
df = pd.read_csv('monthly_sales_data.csv')
df['Month'] = pd.to_datetime(df['Month'])
df.sort_values('Month', inplace=True)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)
app.title = "Tablero de Ventas Mensuales"

# Diseño de la aplicación
app.layout = html.Div([
    html.H1("Tablero de Ventas Mensuales", style={'textAlign': 'center'}),

    # Dropdown para seleccionar categoría
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': cat, 'value': cat} for cat in df['Category'].unique()],
        value=df['Category'].unique()[0],
        clearable=False
    ),

    # RadioItems para seleccionar tipo de gráfico
    dcc.RadioItems(
        id='chart-type',
        options=[
            {'label': 'Líneas', 'value': 'line'},
            {'label': 'Barras', 'value': 'bar'}
        ],
        value='line',
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    # RangeSlider para seleccionar rango de fechas
    dcc.RangeSlider(
        id='date-range',
        min=0,
        max=len(df['Month'].unique()) - 1,
        value=[0, len(df['Month'].unique()) - 1],
        marks={i: date.strftime('%b %Y') for i, date in enumerate(df['Month'].unique())},
        step=1
    ),

    # Botón para cambiar el fondo del gráfico
    html.Button('Cambiar Fondo', id='background-button', n_clicks=0),

    # Gráficos en una estructura de 2x2
    html.Div([
        html.Div(dcc.Graph(id='graph-1'), style={'width': '48%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='graph-2'), style={'width': '48%', 'display': 'inline-block'}),
    ]),
    html.Div([
        html.Div(dcc.Graph(id='graph-3'), style={'width': '48%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='graph-4'), style={'width': '48%', 'display': 'inline-block'}),
    ]),
])

# Callback para actualizar los gráficos
@app.callback(
    Output('graph-1', 'figure'),
    Output('graph-2', 'figure'),
    Output('graph-3', 'figure'),
    Output('graph-4', 'figure'),
    Input('category-dropdown', 'value'),
    Input('chart-type', 'value'),
    Input('date-range', 'value'),
    Input('background-button', 'n_clicks')
)
def update_graphs(selected_category, chart_type, date_range, n_clicks):
    # Filtrar datos por categoría
    filtered_df = df[df['Category'] == selected_category]

    # Filtrar datos por rango de fechas
    months = filtered_df['Month'].unique()
    start_date = months[date_range[0]]
    end_date = months[date_range[1]]
    mask = (filtered_df['Month'] >= start_date) & (filtered_df['Month'] <= end_date)
    filtered_df = filtered_df.loc[mask]

    # Configurar fondo del gráfico
    background_color = '#ffffff' if n_clicks % 2 == 0 else '#f0f0f0'

    # Gráfico 1: Ventas mensuales (líneas)
    fig1 = px.line(filtered_df, x='Month', y='Sales', title='Ventas Mensuales')
    fig1.update_layout(plot_bgcolor=background_color)

    # Gráfico 2: Ventas mensuales (barras)
    fig2 = px.bar(filtered_df, x='Month', y='Sales', title='Ventas Mensuales (Barras)')
    fig2.update_layout(plot_bgcolor=background_color)

    # Gráfico 3: Ventas acumuladas
    filtered_df['Cumulative Sales'] = filtered_df['Sales'].cumsum()
    fig3 = px.area(filtered_df, x='Month', y='Cumulative Sales', title='Ventas Acumuladas')
    fig3.update_layout(plot_bgcolor=background_color)

    # Gráfico 4: Tipo de gráfico seleccionado
    if chart_type == 'line':
        fig4 = px.line(filtered_df, x='Month', y='Sales', title='Ventas Mensuales (Líneas)')
    else:
        fig4 = px.bar(filtered_df, x='Month', y='Sales', title='Ventas Mensuales (Barras)')
    fig4.update_layout(plot_bgcolor=background_color)

    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run_server(debug=True)
