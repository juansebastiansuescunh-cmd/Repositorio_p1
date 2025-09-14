#1. Importar librerías
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

#2. Importar datos
df=pd.read_csv('Tarea_5/df_limpio_1y2.csv')

#3. Importar modelo
bundle = joblib.load(r"C:\Users\adri_\OneDrive\Documentos\Juan Sebastian\LOS ANDES\7. Septimo semestre\Analitica computacional para la toma de decisiones\Proyectos\Proyecto 1\Repositorio_p1\Tarea_5\modelo_mlp_con_columnas.pkl")
model = bundle["modelo"]
feature_names = bundle["columnas"]
row = pd.Series(0.0, index=feature_names)
print(row['active'])




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
notify = [{"label": col.replace("notify_", ""), "value": col} for col in notify_cols]