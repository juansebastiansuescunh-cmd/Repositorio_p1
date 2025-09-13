#1. Importar librerías
import pandas as pd
import dash
from dash import dcc  # dash core components
from dash import html # dash html components 
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

#2. Importar datos
df=pd.read_excel("Tarea_5/Datos_problema2.xlsx")

#3. Análisis general
#3.1  data frame general
df_general= df.groupby(["location", "impact"]).size().unstack(fill_value=0).reset_index()
df_general=df_general[df_general['location']!='?']
df_general['total_incidentes']=df_general['1 - High']+df_general['2 - Medium']+df_general['3 - Low']

df_filtrado=df_general
df_filtrado=df_filtrado.sort_values(by='total_incidentes',ascending=False)
df_filtrado=df_filtrado.head(10)
print(df_filtrado)

#3.2  data frame totales
total_high=df_general['1 - High'].sum()
total_medium=df_general['2 - Medium'].sum()
total_low=df_general['3 - Low'].sum()

datos_totales=[
    ['1 - High',total_high],
    ['2 - Medium',total_medium],
    ['3 - Low',total_low],
]

dict_datos_totales={
    '1 - High':total_high,
    '2 - Medium':total_medium,
    '3 - Low':total_low
}

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

        dcc.Graph(id='pie1',figure=pie_totales),
        dcc.Graph(id='bar1',figure=bar_totales)
    ],style={'display':'flex'}),

    html.Div([
        html.H1(children="Identificación de zonas problemáticas"),

        dcc.Slider(
            id='slider1',
            min=10,
            max=50,
            step=5,
            value=10,
            marks={10:'10',15:'15',20:'20',25:'25',30:'30',35:'35',40:'40',45:'45',50:'50'},
            
        ),

        dcc.Graph(id='bar2'),

        html.Div(id='texto1')
    ]),
    
    html.Div([
        html.H1(children='Diseño de estrategia de cobertura'),
        html.H3(children='Análisis absoluto, relativo y proporcional de incidentes por impacto y ubicación'),
        html.P(children='Seleccione la visualización deseada:'),

        dcc.Dropdown(
            id='drop1',
            options=['Lineal','Logaritimica','Normalizada'],
            value='Lineal',
            style={'width':'50%'}
        ),

        dcc.Graph(id='bar3'),

        html.H3(children='Cobertura absoluta y proporcional de la estrategia'),
        html.P(children='Seleccione la visualización deseada:'),
        dcc.Dropdown(
            id='drop2',
            options=['Pie chart','Bar plot'],
            value='Pie chart',
            style={'width':'50%'}
        )
    ]),


    html.Div([
        dcc.Graph(id='grafico1'),
        dcc.Graph(id='grafico2'),
        dcc.Graph(id='grafico3')    
    ],style={
    'display': 'grid',
    'grid-template-columns': '1fr 1fr 1fr',
    'gap': '10px'
    }),


])

@app.callback(
    Output('bar2', 'figure'),
    [Input('slider1', 'value')])
def update_figure(tamaño):
    df_filtrado=df_general[['location','total_incidentes']]
    df_filtrado=df_filtrado.sort_values(by='total_incidentes',ascending=False)
    df_filtrado=df_filtrado.head(tamaño)
    fig=px.bar(
        df_filtrado,
        x='location',
        y='total_incidentes',
    )
    return fig

@app.callback(
    Output('texto1', 'children'),
    [Input('slider1', 'value')])
def update_figure(tamaño):
    df_filtrado=df_general[['location','total_incidentes']]
    df_filtrado=df_filtrado.sort_values(by='total_incidentes',ascending=False)
    df_filtrado=df_filtrado.head(tamaño)
    problematicas=df_filtrado['total_incidentes'].sum()
    totales=df_general['total_incidentes'].sum()
    procentaje =round(100*(problematicas/totales),2)
    texto=f'Las {tamaño} zonas más problemáticas acumulan un {procentaje}% de los incidentes'

    return texto

@app.callback(
    Output('bar3', 'figure'),
    [Input('slider1', 'value'),
     Input('drop1','value')])
def update_figure(tamaño,tipo):
    df_filtrado=df_general
    df_filtrado=df_filtrado.sort_values(by='total_incidentes',ascending=False)
    df_filtrado=df_filtrado.head(tamaño)
    esperadas = {"1 - High", "2 - Medium", "3 - Low"}
    presentes = [c for c in df_filtrado.columns if c in esperadas]

    df_largo = df_filtrado.melt(
        id_vars=["location"],
        value_vars=presentes,
        var_name="impacto",
        value_name="cantidad"
)
    if tipo=='Lineal':
        fig=px.bar(
            df_largo,
            x='location',
            y='cantidad',
            barmode='stack',
            color='impacto',
            color_discrete_map=colores,

        )     

    if tipo=='Logaritimica':
        df_largo['ln_cantidad']=np.log(df_largo['cantidad'])
        
        fig=px.bar(
        df_largo,
        x='location',
        y='ln_cantidad',
        barmode='group',
        color='impacto',
        color_discrete_map=colores,
    )     
    
    if tipo=='Normalizada':
        totales = df_largo.groupby("location")["cantidad"].transform("sum")
        df_largo["porcentaje"] = df_largo["cantidad"] / totales * 100
        fig = px.bar(
            df_largo,
            x="location",
            y="porcentaje",      
            color="impacto",
            barmode="stack",
            color_discrete_map={"1 - High": "red", "2 - Medium": "blue", "3 - Low": "green"},
        )

    return fig                       

@app.callback(
    [Output('grafico1','figure'),
     Output('grafico2','figure'),
     Output('grafico3','figure')],
    [Input('slider1','value'),
     Input('drop2','value')]
)
def update_figure(tamaño,tipo):
    df_filtrado=df_general
    df_filtrado=df_filtrado.sort_values(by='total_incidentes',ascending=False)
    df_filtrado=df_filtrado.head(tamaño)
    suma_high=df_filtrado['1 - High'].sum()
    suma_medium=df_filtrado['2 - Medium'].sum()
    suma_low=df_filtrado['3 - Low'].sum()

    if tipo=='Pie chart':
        cubierto_high=suma_high/dict_datos_totales['1 - High']
        no_cubierto_high=1-cubierto_high

        cubierto_medium=suma_medium/dict_datos_totales['2 - Medium']
        no_cubierto_medium=1-cubierto_medium

        cubierto_low=suma_low/dict_datos_totales['3 - Low']
        no_cubierto_low=1-cubierto_low

        datos_high=[
            ['cubierto',cubierto_high],
            ['no cubierto',no_cubierto_high]
            ]
        df_high=pd.DataFrame(datos_high,columns=['Cobertura','Porcentajes'])

        datos_medium=[
            ['cubierto',cubierto_medium],
            ['no cubierto',no_cubierto_medium]
            ]
        df_medium=pd.DataFrame(datos_medium,columns=['Cobertura','Porcentajes'])

        datos_low=[
            ['cubierto',cubierto_low],
            ['no cubierto',no_cubierto_low]
            ]
        df_low=pd.DataFrame(datos_low,columns=['Cobertura','Porcentajes'])

        fig1=px.pie(
            df_high,
            values='Porcentajes',
            names='Cobertura',
            color='Cobertura',
            title='Cobertura incidentes de impacto alto'
        )

        fig2=px.pie(
            df_medium,
            values='Porcentajes',
            names='Cobertura',
            color='Cobertura',
            title='Cobertura incidentes de impacto medio'
        )

        fig3=px.pie(
            df_low,
            values='Porcentajes',
            names='Cobertura',
            color='Cobertura',
            title='Cobertura incidentes de impacto bajo'
        )
    if tipo=='Bar plot':
        cubierto_high=suma_high
        no_cubierto_high=dict_datos_totales['1 - High']-cubierto_high

        cubierto_medium=suma_medium
        no_cubierto_medium=dict_datos_totales['2 - Medium']-cubierto_medium

        cubierto_low=suma_low
        no_cubierto_low=dict_datos_totales['3 - Low']-cubierto_low

        datos_high=[
            ['cubierto',cubierto_high],
            ['no cubierto',no_cubierto_high]
            ]
        df_high=pd.DataFrame(datos_high,columns=['Cobertura','Cantidades'])

        datos_medium=[
            ['cubierto',cubierto_medium],
            ['no cubierto',no_cubierto_medium]
            ]
        df_medium=pd.DataFrame(datos_medium,columns=['Cobertura','Cantidades'])

        datos_low=[
            ['cubierto',cubierto_low],
            ['no cubierto',no_cubierto_low]
            ]
        df_low=pd.DataFrame(datos_low,columns=['Cobertura','Cantidades'])

        fig1 = px.bar(
            df_high,
            x="Cobertura",
            y="Cantidades",
            color='Cobertura',
            title='Cobertura incidentes de impacto alto'      
        )

        fig2 = px.bar(
            df_medium,
            x="Cobertura",
            y="Cantidades",
            color='Cobertura',
            title='Cobertura incidentes de impacto medio'      
        )

        fig3 = px.bar(
            df_low,
            x="Cobertura",
            y="Cantidades",
            color='Cobertura',
            title='Cobertura incidentes de impacto bajo'      
        )
    return fig1, fig2, fig3


if __name__ == '__main__':
    app.run(debug=True)