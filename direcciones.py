import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os

from localidades import ClaseLocalidad

load_dotenv()

class ClaseDireccion:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT'),
            ssl_disabled=False
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def obtener_datos(self):
        self.cursor.execute('SELECT * FROM direccion')
        result = self.cursor.fetchall()
        return result
    
    def ingresar_datos(self,calle, numero, piso, departamento, localidad, latitud, longitud):
        self.cursor.execute('INSERT INTO direccion (calle_direccion, numero_direccion, piso_direccion, departamento_direccion, localidad_direccion, latitud_direccion, longitud_direccion) VALUES(%s,%s,%s,%s,%s,%s,%s)',(calle, numero, piso, departamento, localidad, latitud, longitud))
        self.connection.commit()
    
    def obtener_id_direccion (self, calle, numero):
        self.cursor.execute('SELECT id_direccion FROM direccion WHERE calle_direccion = %s AND numero_direccion = %s',(calle, numero))
        id = self.cursor.fetchall()
        return id