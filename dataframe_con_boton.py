import pandas as pd
import streamlit as st

@st.dialog
def df_mostrar_datos(df):
    
data_df = pd.DataFrame(
    {   "Nombre":[
        "Robert Lewandowski",
        "Ayoze Pérez"
    ],
        "Goles": [
            7,
            6
            ],
    }
)
data_df["ver_datos"] = "NO"
hola = st.data_editor(
    data_df,
    column_config={
        "ver_datos": st.column_config.SelectboxColumn(
            "App Category",
            help="The category of the app",
            width="medium",
            options=[
                "NO",
                "SÍ",
            ],
            default=0,  
            required=True,
        )
    },
    hide_index=True,
)

if not(hola.empty):
    df_mostrar = hola[hola["ver_datos"] == "SÍ"]
    if not(df_mostrar.empty):
        st.write(df_mostrar)