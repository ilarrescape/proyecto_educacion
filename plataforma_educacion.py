import streamlit as st
from instituciones import fun_instituciones
from carreras import fun_carrera
from mapa import mapa_interactivo
import time

def login_usuario():
    with st.container(border=True):
        nombre_usuario = st.text_input('Nombre de Usuario:' )
        password_usuario = st.text_input("Ingresar Contraseña", type="password")
        if st.button('Iniciar Sesión'):
                if nombre_usuario == 'admin200' and password_usuario == 'admin20011024':
                    st.session_state.usuario = 'logeado'
                    st.success('Login Exitoso')
                    st.rerun()
                else:
                    st.error('Datos Incorrectos')
                        

def show_home():
    st.title('Bienvenido al SiGA')
    st.header('Sistema de Gestión Académica :school:')
    mapa_interactivo()




def main():    
    
    if 'page' not in st.session_state:
        st.session_state.page = 'sesion_inicio'
    
    
    st.markdown("""
        <style>
            .st-emotion-cache-1gwvy71 h1{
                color: white;
                text-align: center;
            } 
            .st-emotion-cache-8atqhb {
                padding-left: 1em;
                padding-right: 1em;
                padding-bottom:1.5em;
                border-radius: 0.5em;
                border: 1px solid rgba(0, 0, 0, 0.5);
                background-color: #000000;
                
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.title('Menú SiGA')

    
    
    if st.sidebar.button('Inicio', use_container_width=True):
        st.session_state.page = 'sesion_inicio'
    if st.sidebar.button('Instituciones', use_container_width=True):
        st.session_state.page = 'sesion_instituciones'
    if st.sidebar.button('Carreras', use_container_width=True):
        st.session_state.page = 'sesion_carreras'
        
    
    if st.session_state.page == 'sesion_inicio':
        show_home()
    if st.session_state.page == 'sesion_instituciones':
        fun_instituciones()
    if st.session_state.page == 'sesion_carreras':
        fun_carrera()


st.set_page_config(layout="wide")
if 'usuario' not in st.session_state:
    st.session_state.usuario = 'no_logeado'

if st.session_state['usuario'] == 'no_logeado':
    with st.sidebar:
        login_usuario()
    show_home()
elif st.session_state['usuario'] == 'logeado':
    main()

# main()