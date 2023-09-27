import dash
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

from process_data import process_data

app = dash.register_page(__name__, path='/graficos')
materials = pd.read_csv('data/materials.csv')['Material']

df  = pd.read_excel('data/pharmawatch.xlsx')

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
    df_material = df.loc[df['Material'] == material]

    processed_data = process_data(df_material)

    fig = px.line(processed_data['data'], x='Mes Sequencial', y=['Quantidade','Média Móvel + 20%','Q3'],
                labels={'value': 'Quantidade'},
                title='Quantidade Mensal, Média Móvel e Quartis - Período Completo')
    
    for i, d in enumerate(fig.data):
        for j, a in enumerate(d.x):
            fig.add_annotation(x=a, y = d.y[j], text = str(d.y[j])[:5],
                            showarrow = False,
                            yshift = 10,
                            font=dict(color=d.line.color, size=12))   
    
    # fig.add_annotation(x=data['Mes Sequencial'], y=data['Quantidade'], text='Quantidade')
    # fig.add_annotation(x=data['Mes Sequencial'], y=data['Média Móvel + 20%'], text='Média Móvel + 20%')
    # fig.add_annotation(x=data['Mes Sequencial'], y=data['Q75'], text='Q75')

    
    # fig.add_hline(y=processed_data['quantile_25'], line_dash="dash", line_color="gray", name="25% Quartil")
    # fig.add_hline(y=processed_data['quantile_50'], line_dash="dash", line_color="gray", name="50% Quartil")
    # fig.add_hline(y=processed_data['quantile_75'], line_dash="dash", line_color="gray", name="75% Quartil")
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
