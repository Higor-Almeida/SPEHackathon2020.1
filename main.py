from flask import Flask
from flask import render_template
import dash
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
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

#dash app for production
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
        options=[{'label': j, 'value': j} for j in np.sort(pd.unique(df["Operadora"]))
                 ],
        placeholder="Select an Operator",
        multi=True,
        disabled=True
    ),

    dcc.Dropdown(
        id='departamento',
        options=[],
        placeholder="Select a Department",
        multi=True,
        disabled=True
    ),

    dcc.Dropdown(
        id='municipio',
        options=[],
        placeholder="Select a County",
        multi=True,
        disabled=True
    ),

    dcc.Dropdown(
        id='contrato',
        options=[],
        placeholder="Select a Contract",
        multi=True,
        disabled=True
    ),

    dcc.Dropdown(
        id='campo',
        options=[],
        placeholder="Select a Field",
        multi=True,
        disabled=True
    ),

    dcc.Graph(
        id='example-graph',
        figure={}
    ),

    html.Div([
        html.H1(children="Ranking de los Campos"),
        
        dash_table.DataTable(
            id='datatable',
            columns=[{"name":i,"id":i} for i in df.columns],
            page_current=0,
            page_action='custom'
        ),

        html.Br(),
        'Number of Rows: ',
        dcc.Input(
            id='datatable-row-count',
            type="number",
            min=1,
            max=10,
            value=5
        ),

        #dcc.Checklist(
        #    id="datatable-sort-order",
        #    options=[
        #        {"label":"Ascending",'value':"True"}
        #    ],
        #    value=['True']
        #)
    ]),
])

@app.callback(
    dash.dependencies.Output(component_id="example-graph", component_property="figure"),
    [dash.dependencies.Input(component_id='operadoras', component_property='value'),
     dash.dependencies.Input(component_id='ano', component_property='value'),
     dash.dependencies.Input(component_id='mes', component_property='value'),
     dash.dependencies.Input(component_id='departamento', component_property='value'),
     dash.dependencies.Input(component_id='municipio', component_property='value'),
     dash.dependencies.Input(component_id='contrato', component_property='value'),
     dash.dependencies.Input(component_id='campo', component_property='value')]
)
def update_graph(operadora, ano, mes, departamento, municipio, contrato, campo):
    list_parm = [departamento, municipio, contrato, campo]
    list_label = ["Departamento", "Municipio", "Contrato", "Campo"]
    if mes is None or mes == []:
        mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
               'Noviembre', 'Diciembre']
    if operadora is None or operadora == []:
        fil = df[df["Year"].isin(ano)]
        operadora = [i for i in np.sort(pd.unique(fil["Operadora"]))]
    try:
        prod = []
        op = []
        anos = []
        for oper in operadora:
            copy_data = df.copy()
            copy_data = copy_data[copy_data["Operadora"] == oper]
            for year in ano:
                period = copy_data[copy_data["Year"] == year]
                for index in range(4):
                    if list_parm[index] == [] or list_parm[index] is None:
                        pass
                    else:
                        period = period[period[list_label[index]].isin(list_parm[index])]
                prod_cumu = 0
                for month in mes:
                    prod_cumu += period[month].sum()
                prod.append(prod_cumu)
                op.append(oper)
                anos.append(year)
        resp = pd.DataFrame({'Ano': anos, 'Operadoras': op, 'Producion': prod})
        resp = resp.sort_values(by=['Producion', 'Ano'])
        fig = px.bar(resp, x='Ano', y='Producion', color='Operadoras', barmode="group", labels=dict(x='Year', y='Production', color='Operadora'))
        fig.update_xaxes(tick0=2017, dtick=1)
    except:
        print(list_parm[0])
        fig = ""
    return fig

@app.callback(
    [dash.dependencies.Output(component_id="operadoras", component_property="disabled"),
     dash.dependencies.Output(component_id="departamento", component_property="disabled"),
     dash.dependencies.Output(component_id="municipio", component_property="disabled"),
     dash.dependencies.Output(component_id="contrato", component_property="disabled"),
     dash.dependencies.Output(component_id="campo", component_property="disabled"),],
    [dash.dependencies.Input(component_id='ano', component_property='value')]
)
def update_graph_2(ano):
    if ano is None or ano == []:
        b = True
    else:
        b = False
    return b, b, b, b, b

@app.callback(
    [dash.dependencies.Output(component_id="departamento", component_property="options"),
     dash.dependencies.Output(component_id="municipio", component_property="options"),
     dash.dependencies.Output(component_id="contrato", component_property="options"),
     dash.dependencies.Output(component_id="campo", component_property="options")],
    [dash.dependencies.Input(component_id='operadoras', component_property='value'),
     dash.dependencies.Input(component_id='ano', component_property='value')]
)
def update_graph_3(operadora, ano):
    try:
        for i in ano:
            copy = df.copy()
            copy = copy[copy["Year"] == i]
            if operadora is None or operadora == []:
                filt_dep = [j for j in np.sort(pd.unique(copy["Departamento"]))]
                filt_mun = [j for j in np.sort(pd.unique(copy["Municipio"]))]
                filt_con = [j for j in np.sort(pd.unique(copy["Contrato"]))]
                filt_cam = [j for j in np.sort(pd.unique(copy["Campo"]))]
            else:
                for k in operadora:
                    op = copy[copy["Operadora"] == k]
                    filt_dep = [j for j in np.sort(pd.unique(op["Departamento"]))]
                    filt_mun = [j for j in np.sort(pd.unique(op["Municipio"]))]
                    filt_con = [j for j in np.sort(pd.unique(op["Contrato"]))]
                    filt_cam = [j for j in np.sort(pd.unique(op["Campo"]))]
        opt_dep = [{'label': j, 'value': j} for j in np.sort(pd.unique(filt_dep))]
        opt_mun = [{'label': j, 'value': j} for j in np.sort(pd.unique(filt_mun))]
        opt_con = [{'label': j, 'value': j} for j in np.sort(pd.unique(filt_con))]
        opt_cam = [{'label': j, 'value': j} for j in np.sort(pd.unique(filt_cam))]

    except:
        opt_dep = []
        opt_mun = []
        opt_con = []
        opt_cam = []
    return opt_dep, opt_mun, opt_con, opt_cam

@app.callback(
    Output('datatable','data'),
    [Input('datatable-row-count','value')])
def update_table(row_count):
    #Function created to update the ranking table
    try:
        return df.iloc[:row_count,:].to_dict('records')
    except:
        return 20

#url path
@server.route("/production")
def my_dash_app():
    return app.index()

@server.route("/")
def index():
    return render_template('index.html')


#inicia app flask
if __name__ == "__main__":
    server.run(debug=True)

