from flask import Flask
from flask import render_template
import dash
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np

#cria app flask
server = Flask(__name__)

#dash style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#cria app dash
app = dash.Dash(
    __name__,
    server=server, #instancia no app flask
    url_base_pathname='/dash/',
    external_stylesheets=external_stylesheets
)

#carrega base
df = pd.read_excel('colombia_consolidado.xlsx', index_col=0)

#layout da página (no momento só o gráfico e os filtros, ainda faltam alguns filtros)
app.layout = html.Div(children=[
    dcc.Dropdown(
        options=[
            {'label': '2018', 'value': 2018},
            {'label': '2019', 'value': 2019},
            {'label': '2020', 'value': 2020}
        ],
        #value=[],
        multi=True
    ),

    dcc.Dropdown(
        options=[
            {'label': 'Enero', 'value': 'Enero'},
            {'label': 'Febrero', 'value': 'Febrero'},
            {'label': 'Marzo', 'value': 'Marzo'},
            {'label': 'Abril', 'value': 'Abril'},
            {'label': 'Mayo', 'value': 'Mayo'},
            {'label': 'Junio', 'value': 'Junio'},
            {'label': 'Julio', 'value': 'Julio'},
            {'label': 'Agosto', 'value': 'Agosto'},
            {'label': 'Sptiembre', 'value': 'Septiembre'},
            {'label': 'Octubre', 'value': 'Octubre'},
            {'label': 'Noviembre', 'value': 'Noviembre'},
            {'label': 'Diciembre', 'value': 'Diciembre'}
        ],
        #value=[],
        multi=True
    ),

    dcc.Dropdown(
        id='operadoras',
        options=[
            {'label': 'ECOPETROL S.A.', 'value': 'ECOPETROL S.A.'}
        ],
        #value=['ECOPETROL S.A.'],
        multi=True
    ),

    dcc.Graph(
        id='example-graph',
        figure={}
    )
])


#url path
@server.route("/dash")
def my_dash_app():
    return app.index()


@server.route("/")
def index():
    return render_template('index.html')

#funcionalidade dos filtros
@app.callback(
    dash.dependencies.Output(component_id="example-graph", component_property="figure"),
    [dash.dependencies.Input(component_id='operadoras', component_property='value')]
)
def update_graph(operadora):
    container = "{}".format(operadora)
    dff = df.copy()
    dff = dff[dff["Operadora"] == operadora[0]]
    dd = pd.unique(df["Year"])
    prod = []
    op = []
    for i in dd:
        dfff = dff[dff["Year"] == i]
        dffff = dfff["Enero"].sum()
        prod.append(dffff)
        op.append(operadora[0])
    fig = px.bar(x=dd, y=prod, color=op, barmode="group")
    return fig


#inicia app flask
if __name__ == "__main__":
    server.run()



