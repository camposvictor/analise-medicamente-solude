import os

import dash
import pandas as pd
from dash import dcc, html

from process_data import calc_demand, calc_slope

app = dash.register_page(__name__, path='/')

df  = pd.read_excel(os.path.abspath('data/pharmawatch.xlsx'))
materials = pd.read_csv(os.path.abspath('data/materials.csv'))['Material']

df_tendency = pd.DataFrame(columns=['Material', 'Tendência', 'Demanda'])
for material in materials:
    data = df.loc[df['Material'] == material]
    coefficient = calc_slope(data)
    demand = calc_demand(data)

    df_tendency.loc[len(df_tendency)] = {'Material': material, 'Tendência': coefficient, 'Demanda': demand}


df_tendency.sort_values(by='Tendência', ascending=False, inplace=True)

def generate_row(row):
    trend_modifier = 'material-item__number--positive' if row['Tendência'] >= 0 else 'material-item__number--negative'
    demand_modifier = 'material-item__number--positive' if row['Demanda'] >= 0 else 'material-item__number--negative'
    return dcc.Link([
    html.Li([html.P(children=row['Material'], className='material-item__name'), html.Div([html.P("Tendência", className='material-item__label'),html.Div(children=row["Tendência"], className=f'material-item__number {trend_modifier}')], className='material-item__attr'),
            html.Div([html.P('Demanda', className='material-item__label'),html.Div(row["Demanda"], className=f'material-item__number {demand_modifier}')], className='material-item__attr')], className='material-item')
    , ], href=f'/graficos?material={row["Material"]}', style={'textDecoration': 'none'}
    ) 


layout = html.Div(children=[
    html.Ul(
    [generate_row(row) for _,row in df_tendency.iterrows()], className='material-list'
    ),
], style={'maxWidth': '1200px', 'margin': '0 auto'})

if __name__ == '__main__':
    app.run(debug=True)
