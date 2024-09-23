import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os
import time

from orientacion_carreras import ClaseOrientacionCarrera, DataManagerOrientacion
from instituciones import DataManagerInstitucion, ClaseInstitucion
load_dotenv()

class ClaseCarrera:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    def obtener_datos(self):
        consulta = """
                    SELECT 
                        carrera.nombre_carrera as "Carrera",
                        orientacion_carrera.nombre_orientacion_carrera as "Orientación"
                    from
                        carrera
                    join
                        orientacion_carrera on carrera.orientacion_carrera = orientacion_carrera.id_orientacion_carrera
                """
        self.cursor.execute(consulta)
        result = self.cursor.fetchall()
        return result
    
    def agregar_datos(self, nombre, orientacion):
        self.cursor.execute('INSERT INTO carrera (nombre_carrera, orientacion_carrera) VALUES (%s, %s)',(nombre, orientacion))
        self.connection.commit()


class DataManagerCarrera():
    def __init__(self) -> None:
        self.db_orientaciones = ClaseOrientacionCarrera()
        self.db_carreras = ClaseCarrera()
    
    def mostrar_datos(self):
        data_orientaciones = self.db_orientaciones.obtener_datos()
        data_carreras = self.db_carreras.obtener_datos()
        return data_orientaciones, data_carreras
        
    def agregar_registro(self, data_orientaciones, data_carreras):
        nombre_carrera = st.text_input('Nombre: ')
        dic_orientacion_carrera = {row['nombre_orientacion_carrera']:row['id_orientacion_carrera'] for row in data_orientaciones}
        orientacion_carrera = st.selectbox('Orientación', dic_orientacion_carrera.keys()) 
        if st.button('Guardar Nueva Carrera', type='primary', use_container_width=True):
            if nombre_carrera == '':
                st.warning('Debe ingresar un nombre de carrera')
            else:
                self.db_carreras.agregar_datos(nombre_carrera, dic_orientacion_carrera[orientacion_carrera])
                st.success('Registro agregado exitosamente.')
                st.rerun()

def dialog_carrera():
    objeto_carrera = DataManagerCarrera()
    objeto_orientacion = DataManagerOrientacion()
    data_orientaciones, data_carreras = objeto_carrera.mostrar_datos()
    col_a, col_b = st.columns([2, 4])
    with st.container(border=True):
        col_I, col_II = st.columns([2,4])
    with st.container(border=True):
        with col_a:
            with st.container(border= True):
                st.header('Crear Carrera')
                show_new_orientation = False
                show_new_orientation = st.checkbox("Agregar Disciplina", help='Marque para agregar una nueva disciplina.',value = show_new_orientation)
                if show_new_orientation:
                    show_new_orientation = objeto_orientacion.agregar_registro(data_orientaciones)
                else:
                    objeto_carrera.agregar_registro(data_orientaciones, data_carreras)
        
        with col_b:
            df_carreras_filtro = st.dataframe(data_carreras,
                                    use_container_width=True,
                                    height=370,
                                    selection_mode = "multi-row",
                                    on_select='rerun')
            data_carreras = pd.DataFrame(data_carreras)
            if df_carreras_filtro['selection']['rows']:
                with col_II:
                    lista_filtro = df_carreras_filtro.selection['rows']
                    data_filtrada = data_carreras[data_carreras.index.isin(lista_filtro)]
                    st.write(data_filtrada)
                with col_I:
                    objeto_institucion = DataManagerInstitucion()   
                    data_instituciones, data_localidades, data_tipo_instituciones, data_direcciones = objeto_institucion.mostrar_datos()
                    df_instituciones = pd.DataFrame(data_instituciones)
                    dic_instituciones = {row['Nombre']:row['ID'] for row in data_instituciones}
                    institucion_seleccionada = st.selectbox('Seleccione Institución: ',dic_instituciones.keys())