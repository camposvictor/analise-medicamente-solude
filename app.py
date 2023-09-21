import dash
from dash import Dash, dcc, html

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Análise de medicamentos', className="layout-title"),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '0 16px'})

server = app.server

if __name__ == '__main__':
    app.run(debug=True)