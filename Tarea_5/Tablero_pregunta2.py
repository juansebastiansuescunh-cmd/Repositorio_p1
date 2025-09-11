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

dict_datos_totales={
    '1 - High':total_high,
    '2 - Medium':total_medium,
    '3 - Low':total_low
}

print(dict_datos_totales)

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
        html.H1(children='Relación entre impacto y zona')
    ]),

    html.Div([

        dcc.Graph(id='bar3'),

        dcc.Dropdown(
            id='drop1',
            options=['1 - High','2 - Medium','3 - Low'],
            value='1 - High',
            style={'width':'50%'}
        ),

        dcc.Graph(id='pie2')
    ])



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
    [Input('slider1', 'value')])
def update_figure(tamaño):
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

    fig=px.bar(
        df_largo,
        x='location',
        y='cantidad',
        barmode='stack',
        color='impacto',
        color_discrete_map=colores,

    )     
    return fig                       

@app.callback(
    Output('pie2','figure'),
    [Input('slider1','value'),
     Input('drop1','value')]
)
def update_figure(tamaño,tipo):
    df_filtrado=df_general
    df_filtrado=df_filtrado.sort_values(by='total_incidentes',ascending=False)
    df_filtrado=df_filtrado.head(tamaño)
    suma=df_filtrado[tipo].sum()
    totales=dict_datos_totales[tipo]
    cubierto=suma
    p_cubierto=cubierto/totales
    no_cubierto=1-p_cubierto
    datos_porcentajes=[
        ['cubierto',p_cubierto],
        ['no cubierto',no_cubierto]
        ]
    df_porcentajes=pd.DataFrame(datos_porcentajes,columns=['Cobertura','Porcentajes'])
    fig=px.pie(
        df_porcentajes,
        values='Porcentajes',
        names='Cobertura'
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)