from flask import Flask
from flask import render_template
import dash
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

#carrega base
df = pd.read_excel('colombia_consolidado.xlsx')

#cria app flask
server = Flask(__name__)

#dash style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#cria app dash
app = dash.Dash(
    __name__,
    server=server, #instancia no app flask
    url_base_pathname='/production/',
    external_stylesheets=external_stylesheets
)

#layout da página (no momento só o gráfico e os filtros, ainda faltam alguns filtros)
app.layout = html.Div(children=[
    dcc.Dropdown(
        id='ano',
        options=[
            {'label': '2018', 'value': 2018},
            {'label': '2019', 'value': 2019},
            {'label': '2020', 'value': 2020}
        ],
        placeholder="Select a Year",
        multi=True
    ),

    dcc.Dropdown(
        id='mes',
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
        placeholder="Select a Month",
        multi=True
    ),

    dcc.Dropdown(
        id='operadoras',
        options=[{'label': i, 'value': i} for i in np.sort(pd.unique(df["Operadora"]))
                 ],
        placeholder="Select an Operator",
        multi=True,
        disabled=True
    ),

    dcc.Dropdown(
        id='departamento',
        options=[{'label': i, 'value': i} for i in np.sort(pd.unique(df["Departamento"]))
                 ],
        placeholder="Select a Department",
        multi=True
    ),

    dcc.Dropdown(
        id='municipio',
        options=[{'label': i, 'value': i} for i in np.sort(pd.unique(df["Municipio"]))
                 ],
        placeholder="Select a County",
        multi=True
    ),

    dcc.Dropdown(
        id='contrato',
        options=[{'label': i, 'value': i} for i in np.sort(pd.unique(df["Contrato"]))
                 ],
        placeholder="Select a Contract",
        multi=True
    ),

    dcc.Dropdown(
        id='campo',
        options=[{'label': i, 'value': i} for i in np.sort(pd.unique(df["Campo"]))
                 ],
        placeholder="Select a Field",
        multi=True
    ),

    dcc.Graph(
        id='example-graph',
        figure={}
    )
])
m = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre',
     'Diciembre']

@app.callback(
    [dash.dependencies.Output(component_id="example-graph", component_property="figure"),
     dash.dependencies.Output(component_id="operadoras", component_property="disabled")],
    [dash.dependencies.Input(component_id='operadoras', component_property='value'),
     dash.dependencies.Input(component_id='ano', component_property='value'),
     dash.dependencies.Input(component_id='mes', component_property='value')]
)
def update_graph(operadora, ano, mes):
    print(ano)
    if ano is None or ano == []:
        print('entrou if')
        b = True
    else:
        print('entrou else')
        b = False
    if mes is None or mes == []:
        mes = m
    if operadora is None or operadora == []:
        operadora = [i for i in np.sort(pd.unique(df["Operadora"]))]
    try:
        prod = []
        op = []
        anos = []
        for j in operadora:
            copy_data = df.copy()
            copy_data = copy_data[copy_data["Operadora"] == j]
            for i in ano:
                prod_cumu = 0
                period = copy_data[copy_data["Year"] == i]
                for z in mes:
                    prod_cumu += period[z].sum()
                prod.append(prod_cumu)
                op.append(j)
                anos.append(i)
        fig = px.bar(x=anos, y=prod, color=op, barmode="group", labels=dict(x='Year', y='Production', color='Operadora'))
        fig.update_xaxes(tick0=2017, dtick=1)
    except:
        fig = ""
    return fig, b

#url path
@server.route("/production")
def my_dash_app():
    return app.index()


# @server.route("/ranking")
# def my_dash_app_2():
#     return app_2.index()


@server.route("/")
def index():
    return render_template('index.html')


#inicia app flask
if __name__ == "__main__":
    server.run()

