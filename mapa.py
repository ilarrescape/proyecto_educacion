
import streamlit as st
import pydeck as pdk
import pandas as pd
import folium
from streamlit_folium import st_folium

from instituciones import ClaseInstitucion
from localidades import ClaseLocalidad
from carreras import ClaseCarrera
from instituciones_carreras import ClaseInstitucionCarrera, formatear_numero

def cambia_dataframe(data_visual, df_final,**kwargs):  
    for clave,valor in kwargs.items():
            if not(data_visual.empty):
                if valor!= 'Todas':
                    data_visual = data_visual[data_visual[clave] == valor]
            else:
                return 'No se Encontraron Coincidencias'
    return data_visual

def fun_mapa(m, diccionario_instituciones):
    for i in diccionario_instituciones:
        popup_text = f"""
        <strong>{i['Nombre']}</strong><br>
        Dirección: {i['Dirección']}<br>
        Número:{i['N°']}<br>
        Teléfono: {i['Teléfono']}<br>
        Email: {i['Email']}
        """
        icono = folium.Icon(color='red', icon='book')
        folium.Marker([i['Latitud'], i['Longitud']], popup=folium.Popup(popup_text, max_width=300), tooltip=i['Nombre'], icon=icono).add_to(m)



def mapa_interactivo():
    objeto_localidades = ClaseLocalidad()
    objeto_instituciones = ClaseInstitucion()
    objeto_carreras = ClaseCarrera()
    objeto_institucion_carrera = ClaseInstitucionCarrera()
    
    
    
    result, diccionario_instituciones = objeto_instituciones.obtener_datos()
    df_instituciones = pd.DataFrame(diccionario_instituciones)
    df_carreras = pd.DataFrame(objeto_carreras.obtener_datos())
    df_institucion_carrera = pd.DataFrame(objeto_institucion_carrera.obtener_datos())
    
    df_final = pd.merge(df_instituciones,df_institucion_carrera, left_on='ID', right_on='id_institucion', how='inner')
    df_final = pd.merge(df_carreras, df_final, left_on='ID', right_on='id_carrera', how='inner')
    
    m = folium.Map(location=[-37.259411, -56.971661], zoom_start=12, tiles="CartoDB Voyager")
    
    with st.container(border=True):
        col_I,col_II, col_III = st.columns([1,2,1])
        with col_I:
            lista_pub_pri = ['Pública', 'Privado', 'Todas']
            publico_privado = st.selectbox('Gestión: ', lista_pub_pri, index=2, on_change = None)
        with col_III:
            datos_localidades = objeto_localidades.obtener_datos()
            dic_localidades = {row['id_localidad']:row['nombre_localidad']for row in datos_localidades}
            lista_localidades = list(dic_localidades.values())
            lista_localidades.append('Todas')
            localidad = st.selectbox('Localidad: ', lista_localidades, index=len(lista_localidades)-1, on_change = None)
        with col_II:
            lista_tipo_institucion = list(set(df_instituciones['Tipo']))
            lista_tipo_institucion.append('Todas')
            tipo_institucion = st.selectbox('Tipo de Institución', lista_tipo_institucion, index=len(lista_tipo_institucion)-1, on_change = None)
        col_IV, col_V, col_VI = st.columns([3,2,1])
        with col_IV:
            lista_institucion = list(set(df_instituciones['Nombre']))
            lista_institucion.append('Todas')
            institucion =st.selectbox('Institución: ', lista_institucion, index=len(lista_institucion)-1,on_change = None)
        with col_V:
            lista_disciplinas = list(set(df_carreras['Disciplina']))
            lista_disciplinas.append('Todas')
            disciplina = st.selectbox('Disciplina: ', lista_disciplinas, index=len(lista_disciplinas)-1, on_change = None)
        
        with col_VI:
            lista_modalidad = ['Virtual', 'Presencial', 'Mixta', 'Todas']
            modalidad = st.selectbox('Modalidad', lista_modalidad, index=3, on_change = None)
            lista_eliminar = ['ID_x', 'ID_y', 'id_institucion', 'id_carrera','Latitud', 'Longitud']
        lista_carrera = list(set(df_carreras['Carrera']))
        lista_carrera.append('Todas')
        carrera = st.selectbox('Buscar Carrera Específica', lista_carrera, index=(len(lista_carrera)-1))
        df_visual = df_final.drop(columns=lista_eliminar)
        df_visual = df_visual.rename(columns={'modalidad_carrera':'Modalidad'})
        df_final = cambia_dataframe(df_visual, df_final, Gestión = publico_privado, Localidad = localidad, Tipo = tipo_institucion, Nombre = institucion, Disciplina = disciplina, Modalidad = modalidad, Carrera = carrera)
        
        if isinstance(df_final,str):
            st.warning(df_final)
        else:
            df_final['Teléfono'] = df_final['Teléfono'].apply(formatear_numero)
            st.dataframe(df_final, use_container_width=True, height=520)
    fun_mapa(m, diccionario_instituciones)
    st_folium(m,height=518, width='100%')


    
    