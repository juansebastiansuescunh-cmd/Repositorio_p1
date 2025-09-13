#1. Importar librerías
import pandas as pd
import dash
from dash import dcc  # dash core components
from dash import html # dash html components 
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

#2. Importar datos
df=pd.read_csv('df_limpio_1y2.csv')

#3. Importar modelo