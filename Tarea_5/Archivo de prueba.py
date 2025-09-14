#1. Importar librerías
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

#2. Importar datos
df=pd.read_csv('Tarea_5/df_limpio_1y2.csv')

#3. Importar modelo
bundle = joblib.load("modelo_mlp_con_columnas.pkl")







