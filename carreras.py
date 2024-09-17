import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os

from orientacion_carreras import ClaseOrientacionCarrera
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
    
#     def actualizar_datos(self, id, nombre, direccion, tipo, telefono, email, gestion):
#         consulta_actualzar = 'UPDATE institucion SET nombre_institucion = %s, direccion_institucion = %s, tipo_institucion = %s, telefono_institucion = %s, email_institucion = %s, gestion_institucion = % WHERE id_institucion = %s'
        
#         self.cursor.execute('UPDATE institucion SET nombre_institucion = %s, direccion_institucion = %s, tipo_institucion = %s, telefono_institucion = %s, email_institucion = %s, gestion_institucion = %s WHERE id_institucion = %s', (nombre, direccion, tipo, telefono, email, gestion, id))
#         self.connection.commit()
#     def eliminar_datos (self, id):
#         self.cursor.execute('DELETE FROM institucion WHERE id_institucion = %s', (id,))

# class DataManagerInstitucion():
#     def __init__(self) -> None:
#         self.db_localidades = ClaseLocalidad()
#         self.db_instituciones = ClaseInstitucion()
#         self.db_tipo_instituciones = ClaseTipoInstitucion()
#         self.db_direcciones = ClaseDireccion()
    
#     def mostrar_datos(self):
#         data_instituciones, diccionario_instituciones = self.db_instituciones.obtener_datos()
#         data_localidades =self.db_localidades.obtener_datos()
#         data_tipo_instituciones = self.db_tipo_instituciones.obtener_datos()
#         data_direcciones = self.db_direcciones.obtener_datos()
        
#         return data_instituciones, data_localidades, data_tipo_instituciones, data_direcciones
        
#     def agregar_registro(self, data_instituciones, data_localidades, data_tipo_instituciones, data_direcciones):
#         with st.container(border= True):
#             col_I, col_II = st.columns(2)
#             with col_I:
#                 with st.container(border=True):
#                     st.header('Agregar Institución')
#                     nombre_institucion = st.text_input('Nombre: ')
#                     col_tel, col_email = st.columns(2)
#                     with col_tel:
#                         telefono_institucion = st.number_input('Teléfono: ', value=0, format="%d", step=1)
#                     with col_email:
#                         email_institucion = st.text_input('Correo Electrónico: ')
#                     col_III, col_IV = st.columns([5,2])
#                     with col_III:
#                         dic_tipo_institucion ={row['nombre_tipo_institucion']:row['id_tipo_institucion'] for row in  data_tipo_instituciones}
#                         tipo_institucion = st.selectbox('Tipo de Institución: ', dic_tipo_institucion.keys())
#                     with col_IV:
#                         lista_gestión = ['Publica','Privada']
#                         gestión_institucion = st.selectbox('Gestión: ', lista_gestión)
#             with col_II:
#                 with st.container(border=True):
#                     st.header('Agregar Dirección')
#                     col_loc, col_call = st.columns([2,3])
#                     with col_loc:
#                         dic_localidad ={row['nombre_localidad']:row['id_localidad'] for row in  data_localidades}
#                         localidad_institucion = st.selectbox('Localidad: ',dic_localidad.keys())
#                     with col_call:
#                         calle_direccion = st.text_input('Calle: ')
#                     col_1, col_2, col_3 = st.columns([1,1,1])
#                     with col_1:
#                         numero_direccion = st.number_input('Número: ', value=0, format="%d", step=1)
#                     with col_2:
#                         piso_direccion = st.text_input('Piso: ')
#                     with col_3:
#                         departamento_direccion = st.text_input('Depto: ')
#                     col_lat, col_long = st.columns(2)
#                     with col_lat:
#                         latitud_direccion = st.number_input('Latitud: ')
#                     with col_long:
#                         longitud_direccion = st.number_input('Longitud: ')
#             c1,c2 = st.columns([8,1])
#             with c2:
#                 if st.button('Agregar Datos', use_container_width=True):
#                     if not nombre_institucion:
#                         with col_I:
#                             st.error('Falta el nombre de la institución')
#                     elif not calle_direccion:
#                         with col_II:
#                             st.error('Falta la calle de la institucion')
#                     else:
#                         self.db_direcciones.ingresar_datos(calle_direccion,numero_direccion,piso_direccion, departamento_direccion, dic_localidad[localidad_institucion], latitud_direccion,longitud_direccion)
#                         lista_id_direccion = self.db_direcciones.obtener_id_direccion(calle_direccion, numero_direccion)
#                         self.db_instituciones.agregar_datos(nombre_institucion, lista_id_direccion[0]['id_direccion'], dic_tipo_institucion[tipo_institucion], telefono_institucion, email_institucion, gestión_institucion)
#                         st.rerun()


objeto_carrera = ClaseCarrera()
st.write(objeto_carrera.obtener_datos())
objeto_carrera.agregar_datos('Tecnicatura Superior en Análisis de Sistemas', 7)
st.write(objeto_carrera.obtener_datos())
