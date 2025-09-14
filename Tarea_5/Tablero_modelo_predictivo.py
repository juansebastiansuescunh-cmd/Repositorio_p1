
#1. Importar librerías
import pandas as pd
import dash
from dash import dcc  # dash core components
from dash import html # dash html components 
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, log_loss, recall_score
import joblib

#2. Importar datos
df=pd.read_csv('Tarea_5/df_limpio_1y2.csv')

#3. Importar modelo ya realizado por Cesar
bundle = joblib.load(r"C:\Users\adri_\OneDrive\Documentos\Juan Sebastian\LOS ANDES\7. Septimo semestre\Analitica computacional para la toma de decisiones\Proyectos\Proyecto 1\Repositorio_p1\Tarea_5\modelo_mlp_con_columnas.pkl")
model = bundle["modelo"]
feature_names = bundle["columnas"]
row = pd.Series(0, index=feature_names, dtype=float)

#4. Crear display en Dash

#   4.1 Graficos generales
df=pd.read_csv('Tarea_5/df_limpio_1y2.csv')
y=df['made_sla']
conteo = y.value_counts().reset_index()
conteo.columns = ['Valor', 'Cantidad']
conteo['Valor'] = conteo['Valor'].map({1: 'Cumplido', 0: 'No cumplido'})
pie_resueltos=px.pie(conteo,names='Valor',values='Cantidad',color='Valor')
bar_resueltos=px.bar(conteo,x='Valor',y='Cantidad',color='Valor')

loc_cols = [c for c in feature_names if c.startswith("location_")]
options_loc = [{"label": col.replace("location_", ""), "value": col} for col in loc_cols]

cat_cols = [c for c in feature_names if c.startswith("category_")]
options_cat = [{"label": col.replace("category_", ""), "value": col} for col in cat_cols]

subcat_cols = [c for c in feature_names if c.startswith("subcategory_")]
options_subcat = [{"label": col.replace("subcategory_", ""), "value": col} for col in subcat_cols]

state_cols = [c for c in feature_names if c.startswith("incident_state_")]
options_state = [{"label": col.replace("incident_state_", ""), "value": col} for col in state_cols]

contact_cols = [c for c in feature_names if c.startswith("contact_type_")]
options_contact = [{"label": col.replace("contact_type_", ""), "value": col} for col in contact_cols]

impact_cols = [c for c in feature_names if c.startswith("impact_")]
options_impact = [{"label": col.replace("impact_", ""), "value": col} for col in impact_cols]

priority_cols = [c for c in feature_names if c.startswith("priority_")]
options_priority = [{"label": col.replace("contact_type_", ""), "value": col} for col in priority_cols]

notify_cols = [c for c in feature_names if c.startswith("notify_")]
options_notify = [{"label": col.replace("notify_", ""), "value": col} for col in notify_cols]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([

    html.Div([

    html.H1(children='Modelo de predicción: Cumplimiento de acuerdo de calidad'),

    html.H3(children='Estadisticas generales'),

    ]),

    html.Div([
        dcc.Graph(id='pie resueltos',figure=pie_resueltos),
        dcc.Graph(id='bar resueltos',figure=bar_resueltos),
    ],style={'display':'flex'}),

    html.Div([

        html.P(children='El modelo planteado tiene un accuracy del 97%'),
         
        html.H3(children='Parámetros del modelo'),

        html.Label('¿La solicitud está activa?'),
        dcc.Dropdown(
            id="activo",
            options=[{"label": "Si", "value": 1},
                     {"label": "No", "value": 0}],
            value=0,
            style={'width':'75%'}
        ),


        html.Label("Ingresa el numero de veces que se ha reasignado el incidente"),
        dcc.Input(
            id="reassingment_count",
            type="number",       
            value=0             
        ),

        html.Label("Ingresa el numero de veces que se ha reabierto el incidente"),
        dcc.Input(
            id="reopen_count",
            type="number",       
            value=0             
        ),

        html.Label("Ingresa el numero de veces que se ha actualizado el incidente"),
        dcc.Input(
            id="sys_mod_count",
            type="number",       
            value=0             
        ),

        dcc.Dropdown(
            id='Knowledge',
            options=[
            {"label": "Sí", "value": 1},
            {"label": "No", "value": 0}
            ],
            placeholder="¿Se utilizó conocimiento de la base para solucionar el incidente?",
            style={'width':'75%'}
        ),

        dcc.Dropdown(
            id='u_priority',
            options=[
            {"label": "Sí", "value": 1},
            {"label": "No", "value": 0}
            ],
            placeholder="¿El campo de prioridad fue verificado?",
            style={'width':'75%'}
        ),

        dcc.Dropdown(
            id='location',
            options=options_loc,
            placeholder="Seleccione una ubicación",
            style={'width':'75%'}
        ),

        dcc.Dropdown(
            id='cat',
            options=options_cat,
            placeholder="Seleccione una categoria",
            style={'width':'75%'}
        ),

        dcc.Dropdown(
            id='subcat',
            options=options_subcat,
            placeholder="Seleccione una subcategoria",
            style={'width':'75%'}
        ),

        dcc.Dropdown(
            id='state',
            options=options_state,
            placeholder="Seleccione un estado",
            style={'width':'75%'}
        ),

        dcc.Dropdown(
            id='contact',
            options=options_contact,
            placeholder="Seleccione un metodo de contacto",
            style={'width':'75%'}
        ),

        dcc.Dropdown(
            id='impact',
            options=options_impact,
            placeholder="Seleccione un nivel de impacto",
            style={'width':'75%'}
        ),

        dcc.Dropdown(
            id='priority',
            options=options_priority,
            placeholder="Seleccione un nivel de prioridad",
            style={'width':'75%'}
        ),

        dcc.Dropdown(
            id='notify',
            options=options_notify,
            placeholder="Seleccione si se generaron notificaciones ",
            style={'width':'75%'}
        ),

        html.H3(children='Predecir cumplimiento'),

        html.P(id='x_new')

    ])

])

@app.callback(
    Output('x_new', 'children'),
    [Input('activo', 'value'),
     Input('reassingment_count', 'value'),
     Input('reopen_count', 'value'),
     Input('sys_mod_count', 'value'),
     Input('Knowledge', 'value'),
     Input('u_priority', 'value'),
     Input('location', 'value'),
     Input('cat', 'value'),
     Input('subcat', 'value'),
     Input('state', 'value'),
     Input('contact', 'value'),
     Input('impact', 'value'),
     Input('priority', 'value'),
     Input('notify', 'value')])
def crear_x_new(activo,rea_count,reo_count,sys_count,knowledge,u_prio,loc,cat,subcat,state,contact,impact,priority,notify):
    row = pd.Series(0, index=feature_names, dtype=float)
    row['active']=activo
    row['reassignment_count']=rea_count
    row['reopen_count']=reo_count
    row['sys_mod_count']=sys_count
    row[knowledge]=1
    row[u_prio]=1
    row[loc]=1
    row[cat]=1
    row[subcat]=1
    row[state]=1
    row[contact]=1
    row[impact]=1
    row[priority]=1
    row[notify]=1
    X_new = pd.DataFrame([row.values], columns=[str(c) for c in row.index]).astype(float)

    cols_model = [str(c) for c in feature_names]
    X_new = X_new.reindex(columns=cols_model, fill_value=0.0)
    y_prob = model.predict_proba(X_new)[:, 1][0]
    y_pred = model.predict(X_new)[0]
    return f"Prob. de cumplir SLA: {y_prob:.2%} | Predicción: {int(y_pred)}"

if __name__ == '__main__':
    app.run(debug=True)

