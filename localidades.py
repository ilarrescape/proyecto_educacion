import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os

from provincias import ClaseProvincia

load_dotenv()

class ClaseLocalidad:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    def obtener_datos(self):
        self.cursor.execute('SELECT * FROM localidad')
        result = self.cursor.fetchall()
        return result