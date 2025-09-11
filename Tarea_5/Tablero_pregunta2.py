#1. Importar librerías
import pandas as pd
import dash
from dash import dcc  # dash core components
from dash import html # dash html components 
from dash.dependencies import Input, Output
import plotly.express as px

#2. Importar datos
df=pd.read_excel("Tarea_5/Datos_problema2.xlsx")

#3. Análisis general
#3.1  data frame general
df_general= df.groupby(["location", "impact"]).size().unstack(fill_value=0).reset_index()
df_general=df_general[df_general['location']!='?']
df_general['total_incidentes']=df_general['1 - High']+df_general['2 - Medium']+df_general['3 - Low']

#3.2  data frame totales
total_high=df_general['1 - High'].sum()
total_medium=df_general['2 - Medium'].sum()
total_low=df_general['3 - Low'].sum()

datos_totales=[
    ['1 - High',total_high],
    ['2 - Medium',total_medium],
    ['3 - Low',total_low],
]

df_totales=pd.DataFrame(datos_totales,columns=['Impacto','Total'])

colores = {
    "1 - High": "red",
    "2 - Medium": "blue",
    "3 - Low": "green"
}

bar_totales=px.bar(df_totales,x='Impacto',y='Total',color='Impacto',color_discrete_map=colores)
pie_totales=px.pie(df_totales,names='Impacto',values='Total',color='Impacto',color_discrete_map=colores)


#4. Dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.Div([
        html.H1(children='Análisis general de los diferentes tipos de impacto')
    ]),

    html.Div([

        dcc.Graph(id='pie_totales',figure=pie_totales),
        dcc.Graph(id='bar_totales',figure=bar_totales)
    ],style={'display':'flex'}),

    html.Div([
        html.H1(children='Relación entre impacto y zona')
    ]),



])
if __name__ == '__main__':
    app.run(debug=True)