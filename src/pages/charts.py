import os

import dash
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

from api import get_all_materials
from process_data import process_data

app = dash.register_page(__name__, path='/graficos')
materials = get_all_materials()

df  = pd.read_excel(os.getcwd() + '/data/pharmawatch.xlsx')

def layout(material=materials[0]):
    return html.Div([
        html.H2(children='Gráfico', className='chart_title'),
        dcc.Dropdown(materials, material, id='dropdown-selection', className='dropdown'),
        dcc.Graph(id='graph-content', style={'height': '800px'})
    ], style={'maxWidth': '1200px', 'margin': '0 auto'})

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(material):
    data = df.loc[df['Material'] == material]

    processed_data = process_data(data)
    fig = px.line(processed_data['data'], x='Mes Sequencial', y=['Quantidade', 'Média Móvel', 'Média Móvel + 20%', 'Q25', 'Q50', 'Q75'],
                labels={'value': 'Quantidade'},
                title='Quantidade Mensal, Média Móvel e Quartis - Período Completo')
    
    fig.add_hline(y=processed_data['quantile_25'], line_dash="dash", line_color="gray", name="25% Quartil")
    fig.add_hline(y=processed_data['quantile_50'], line_dash="dash", line_color="gray", name="50% Quartil")
    fig.add_hline(y=processed_data['quantile_75'], line_dash="dash", line_color="gray", name="75% Quartil")

    return fig

if __name__ == '__main__':
    app.run(debug=True)
