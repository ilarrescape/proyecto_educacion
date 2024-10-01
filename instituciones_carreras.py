import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os
import time

from instituciones import DataManagerInstitucion, ClaseInstitucion, formatear_numero
load_dotenv()

class ClaseInstitucionCarrera:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    def obtener_datos(self):
        consulta = "SELECT * FROM institucion_has_carrera"
        self.cursor.execute(consulta)
        result = self.cursor.fetchall()
        return result
    
    def agregar_datos(self, id_institucion, id_carrera, modalidad_carrera):
        self.cursor.execute('INSERT INTO institucion_has_carrera (id_institucion, id_carrera, modalidad_carrera) VALUES (%s, %s,%s)',(id_institucion, id_carrera, modalidad_carrera))
        self.connection.commit()

class ManagerInstitucionCarrera:
    def __init__(self) -> None:
        self.db_inst_carreras = ClaseInstitucionCarrera()
        self.db_instituciones = ClaseInstitucion()
        self.db_carreras = ClaseInstitucionCarrera()
    
    def mostrar_instituciones_carreras(self):
        df_instituciones_carreras = pd.DataFrame(self.db_inst_carreras)
        return df_instituciones_carreras

    def ingresar_instituciones_carreras(self,df_carreras_filtro, data_carreras):
        with st.container(border= True):
            with st.expander('Expandir para ver los datos seleccionados'):
                lista_filtro = df_carreras_filtro.selection['rows']
                data_filtrada = data_carreras[data_carreras.index.isin(lista_filtro)]
                data_filtrada['Virtual'] = False
                data_filtrada = data_filtrada.drop(columns =['Disciplina',])
                
                datos_a_ingresar = st.data_editor(
                    data_filtrada,
                    hide_index=True, 
                    disabled=('Carrera','ID'),
                    use_container_width= True
                    )
                mensaje = """
                :bulb: Expanda para seleccionar las **carreras virtuales**.
                Por defecto, se guardan como presenciales.
                """
            st.info(mensaje)
            
        objeto_institucion = DataManagerInstitucion()   
        data_instituciones, data_localidades, data_tipo_instituciones, data_direcciones = objeto_institucion.mostrar_datos()
        df_instituciones = pd.DataFrame(data_instituciones)
        dic_instituciones = {row['Nombre']:row['ID'] for row in data_instituciones}
        institucion_seleccionada = st.selectbox('Seleccione Institución: ',dic_instituciones.keys())
        id_institucion = dic_instituciones[institucion_seleccionada]
        if st.button('Guardar Datos'):
            try:        
                for index, row in datos_a_ingresar.iterrows():
                    vir_pres = 'Presencial'
                    if row["Virtual"] == True:
                        vir_pres = 'Virtual'
                    else:
                        vir_pres = 'Presencial'
                    
                    self.db_carreras.agregar_datos(id_institucion, row["ID"], vir_pres)
                st.success('Datos cargados correctamente :sunglasses:')
                time.sleep(2)
                st.rerun()
            except mysql.connector.IntegrityError as e:
                st.warning(f'La Institución __{institucion_seleccionada}__ ya tiene asociada la carrera __{row["Carrera"]}__')
