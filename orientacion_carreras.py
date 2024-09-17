import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

class ClaseOrientacionCarrera:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    def obtener_datos(self):
        self.cursor.execute('SELECT * FROM orientacion_carrera')
        result = self.cursor.fetchall()
        return result
    
    def agregar_datos(self,nombre_orientacion):
        self.cursor.execute('INSERT INTO orientacion_carrera(nombre_orientacion_carrera) VALUES (%s)',(nombre_orientacion,))
        self.connection.commit()
