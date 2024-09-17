
import streamlit as st
import pydeck as pdk
import pandas as pd
import folium
from streamlit_folium import st_folium

from instituciones import ClaseInstitucion
from localidades import ClaseLocalidad


st.set_page_config(layout="wide")
def fun_mapa(m, diccionario_instituciones):
    for i in diccionario_instituciones:
        popup_text = f"""
        <strong>{i['Nombre']}</strong><br>
        Dirección: {i['Direccion']}<br>
        Número:{i['N°']}<br>
        Teléfono: {i['Teléfono']}<br>
        Email: {i['Email']}
        """
        icono = folium.Icon(color='red', icon='book')
        folium.Marker([i['Latitud'], i['Longitud']], popup=folium.Popup(popup_text, max_width=300), tooltip=i['Nombre'], icon=icono).add_to(m)

objeto_instituciones = ClaseInstitucion()
result, diccionario_instituciones = objeto_instituciones.obtener_datos()

df_instituciones = pd.DataFrame(diccionario_instituciones)

m = folium.Map(location=[-37.259411, -56.971661], zoom_start=12, tiles="CartoDB Voyager")

col_1,col_2 = st.columns(2)
with col_1:
    with st.container(border=True):
        fun_mapa(m, diccionario_instituciones)
        st_folium(m, width=650)
with col_2:
    with st.container(border=True):
        lista_pub_pri = ['Publico', 'Privado']
        st.selectbox('Seleccionar Gestión: ', lista_pub_pri)
        objeto_localidades = ClaseLocalidad()
        datos_localidades = objeto_localidades.obtener_datos()
        dic_localidades = {row['id_localidad']:row['nombre_localidad']for row in datos_localidades}
        st.selectbox('Seleccionar Localidad: ', dic_localidades.values())
        lista_institucion = list(df_instituciones['Nombre'])
        st.selectbox('Seleccionar Institucion: ', lista_institucion)