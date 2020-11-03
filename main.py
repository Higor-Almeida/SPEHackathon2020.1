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
df = pd.read_excel('files\colombia_consolidado.xlsx')

#cria app flask
server = Flask(__name__)

#dash style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#cria app dash
app = dash.Dash(
    __name__,
    server=server, #instancia no app flask
    url_base_pathname='/production_5/',
    external_stylesheets=external_stylesheets
)

#layout da página (no momento só o gráfico e os filtros, ainda faltam alguns filtros)
app.layout = html.Div(children=[
    dcc.Dropdown(
        id='year',
        options=[
            {'label': i, 'value': i} for i in np.sort(pd.unique(df["Year"]))
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

labels_id = ['operadoras', 'year', 'mes','departamento','municipio','contrato','campo']

@app.callback(
    [dash.dependencies.Output(component_id="example-graph", component_property="figure"),
     dash.dependencies.Output(component_id="operadoras", component_property="disabled")],
     [dash.dependencies.Input(component_id=id, component_property="value") for id in labels_id]
)

def update_graph(operadora, year, mes,departamento,municipio,contrato,campo):
    list_params = [operadora,year,mes,departamento,municipio,contrato,campo] #With all our objects
    out_params = [] #Empty list to fill with None or "" values
    for param in list_params: #runs through our params
        if param is None or param == []: #checks if None (first run) or empty
            try:
                out_list.append(param) #adds empty or None to out_list to get all values from this column
                list_params.remove(param) #
            except:
                pass
    if year is None or year == []:
        b = True
    else:
        b = False
    if mes is None or mes == []:
        mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre','Diciembre']
    if operadora is None or operadora == []:
        operadora = [i for i in np.sort(pd.unique(df["Operadora"]))]
    try:
        #df_out = df.copy()
        #list_params.append('Enero')
        #df_out = df_out[df_out.columns & list_params]
        #fig = px.bar(x=years, y=prod, color=op, barmode="group", labels=dict(x='Year', y='Production', color='Operadora')) #original functions
        #fig = px.bar(df_out, x='Year', y='Enero')
        #fig.update_xaxes(tick0=2017, dtick=1)
        fig = px.bar(df, x='Year', y='Enero')
        return fig, b
    except:
        fig = px.bar(df, x='Year', y='Febrero')
        return fig, b
    return fig, b

#url path
@server.route("/production_5/")
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
    server.run(debug=True)