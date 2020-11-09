from flask import Flask
from flask import render_template
import dash
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

#carrega base
df = pd.read_excel('processado.xlsx')

month_cols = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre',
                  'Octubre','Noviembre','Diciembre']

params = {"Enero":31,"Febrero":28,"Marzo":31,"Abril":30,"Mayo":31,"Junio":30,"Julio":31,
          "Agosto":31,"Septiembre":30,"Octubre":31,"Noviembre":30,"Diciembre":31}
df[month_cols] = df[month_cols].assign(**params).mul(df[month_cols])

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
# server = app.server

#layout da página (no momento só o gráfico e os filtros, ainda faltam alguns filtros)
app.layout = html.Div(children=[
    dcc.Dropdown(
        id='sel',
        options=[
            {'label': 'Operadora', 'value': 'Operadora'},
            {'label': 'Departamento', 'value': 'Departamento'},
            {'label': 'Municipio', 'value': 'Municipio'},
            {'label': 'Contrato', 'value': 'Contrato'},
            {'label': 'Campo', 'value': 'Campo'}
        ],
        placeholder="Select an option",
        value='Operadora',
        multi=False,
    ),

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

])

@app.callback(
    [dash.dependencies.Output(component_id="example-graph", component_property="figure"),
     dash.dependencies.Output(component_id="operadoras", component_property="options"),
     dash.dependencies.Output(component_id="departamento", component_property="options"),
     dash.dependencies.Output(component_id="municipio", component_property="options"),
     dash.dependencies.Output(component_id="contrato", component_property="options"),
     dash.dependencies.Output(component_id="campo", component_property="options")],
    [dash.dependencies.Input(component_id='operadoras', component_property='value'),
     dash.dependencies.Input(component_id='ano', component_property='value'),
     dash.dependencies.Input(component_id='mes', component_property='value'),
     dash.dependencies.Input(component_id='departamento', component_property='value'),
     dash.dependencies.Input(component_id='municipio', component_property='value'),
     dash.dependencies.Input(component_id='contrato', component_property='value'),
     dash.dependencies.Input(component_id='campo', component_property='value'),
     dash.dependencies.Input(component_id='sel', component_property='value')]
)
def update_graph(operadora, ano, mes, departamento, municipio, contrato, campo, sel):
    list_parm = [operadora, ano, departamento, municipio, contrato, campo]
    list_label = ["Operadora", "Year", "Departamento", "Municipio", "Contrato", "Campo"]
    if mes is None or mes == []:
        mes = month_cols
    try:
        for o in range(6):
            if sel == list_label[o]:
                q = list_parm[o]
                if q == [] or q is None:
                    fil = df[df["Year"].isin(ano)]
                    q = [i for i in np.sort(pd.unique(fil[sel]))]
                    list_parm[o] = q
        prod = []
        op = []
        anos = []
        for oper in q:
            copy_data = df.copy()
            copy_data = copy_data[copy_data[sel] == oper]
            for year in ano:
                period = copy_data[copy_data["Year"] == year]
                for index in range(6):
                    if list_parm[index] == [] or list_parm[index] is None or list_label[index] == sel or index == 1:
                        pass
                    else:
                        period = period[period[list_label[index]].isin(list_parm[index])]
                prod_cumu = 0
                for month in mes:
                    prod_cumu += period[month].sum()
                prod.append(prod_cumu)
                op.append(oper)
                anos.append(year)
        resp = pd.DataFrame({'Ano': anos, sel: op, 'Producion': prod})
        resp = resp.sort_values(by=['Producion'], ascending=False)
        fig = px.bar(resp, x='Ano', y='Producion', color=sel, barmode="group", labels={'Producion': 'Producion (STB/d)'})
        fig.update_xaxes(tick0=2017, dtick=1)

        opt_1 = df.copy()
        opt_2 = df.copy()
        opt_3 = df.copy()
        opt_4 = df.copy()
        opt_5 = df.copy()
        for index in range(6):
            if list_parm[index] == [] or list_parm[index] is None:
                pass
            else:
                if list_label[index] == 'Operadora':
                    opt_2 = opt_2[opt_2[list_label[index]].isin(list_parm[index])]
                    opt_3 = opt_3[opt_3[list_label[index]].isin(list_parm[index])]
                    opt_4 = opt_4[opt_4[list_label[index]].isin(list_parm[index])]
                    opt_5 = opt_5[opt_5[list_label[index]].isin(list_parm[index])]
                elif list_label[index] == 'Departamento':
                    opt_1 = opt_1[opt_1[list_label[index]].isin(list_parm[index])]
                    opt_3 = opt_3[opt_3[list_label[index]].isin(list_parm[index])]
                    opt_4 = opt_4[opt_4[list_label[index]].isin(list_parm[index])]
                    opt_5 = opt_5[opt_5[list_label[index]].isin(list_parm[index])]
                elif list_label[index] == 'Municipio':
                    opt_1 = opt_1[opt_1[list_label[index]].isin(list_parm[index])]
                    opt_2 = opt_2[opt_2[list_label[index]].isin(list_parm[index])]
                    opt_4 = opt_4[opt_4[list_label[index]].isin(list_parm[index])]
                    opt_5 = opt_5[opt_5[list_label[index]].isin(list_parm[index])]
                elif list_label[index] == 'Contrato':
                    opt_1 = opt_1[opt_1[list_label[index]].isin(list_parm[index])]
                    opt_2 = opt_2[opt_2[list_label[index]].isin(list_parm[index])]
                    opt_3 = opt_3[opt_3[list_label[index]].isin(list_parm[index])]
                    opt_5 = opt_5[opt_5[list_label[index]].isin(list_parm[index])]
                elif list_label[index] == 'Campo':
                    opt_1 = opt_1[opt_1[list_label[index]].isin(list_parm[index])]
                    opt_2 = opt_2[opt_2[list_label[index]].isin(list_parm[index])]
                    opt_3 = opt_3[opt_3[list_label[index]].isin(list_parm[index])]
                    opt_4 = opt_4[opt_4[list_label[index]].isin(list_parm[index])]
                else:
                    opt_1 = opt_1[opt_1[list_label[index]].isin(list_parm[index])]
                    opt_2 = opt_2[opt_2[list_label[index]].isin(list_parm[index])]
                    opt_3 = opt_3[opt_3[list_label[index]].isin(list_parm[index])]
                    opt_4 = opt_4[opt_4[list_label[index]].isin(list_parm[index])]
                    opt_5 = opt_5[opt_5[list_label[index]].isin(list_parm[index])]
        opt_ope = [{'label': j, 'value': j} for j in np.sort(pd.unique(opt_1['Operadora']))]
        opt_dep = [{'label': j, 'value': j} for j in np.sort(pd.unique(opt_2['Departamento']))]
        opt_mun = [{'label': j, 'value': j} for j in np.sort(pd.unique(opt_3['Municipio']))]
        opt_con = [{'label': j, 'value': j} for j in np.sort(pd.unique(opt_4['Contrato']))]
        opt_cam = [{'label': j, 'value': j} for j in np.sort(pd.unique(opt_5['Campo']))]
    except:
        opt_ope = []
        opt_dep = []
        opt_mun = []
        opt_con = []
        opt_cam = []
        fig = ""
    return fig, opt_ope, opt_dep, opt_mun, opt_con, opt_cam

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
    dash.dependencies.Output('datatable', 'data'),
    [dash.dependencies.Input('datatable-row-count', 'value')])
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

