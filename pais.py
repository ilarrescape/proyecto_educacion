import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

class ClasePais:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    def obtener_datos(self):
        self.cursor.execute('SELECT * FROM pais')
        result = self.cursor.fetchall()
        return result
    
    def agregar_datos(self,nombre_pais):
        self.cursor.execute('SELECT * FROM pais order by id_pais desc limit 1')
        lista_diccionario_pais = self.cursor.fetchall()
        return lista_diccionario_pais

objeto_pais = ClasePais()

st.write(objeto_pais.agregar_datos('Paraguay'))



