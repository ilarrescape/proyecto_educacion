import streamlit as st

def show_home():
    st.title('Bienvenido al SiGA')
    st.header('Sistema de Gestión Académica :school:')
    st.balloons()

def show_perfil():
    st.title('Acá va tu info de perfil')
    
if 'page' not in st.session_state:
    st.session_state.page = 'Inicio'

if st.sidebar.button('Inicio'):
    st.session_state.page = 'Inicio'
if st.sidebar.button('Perfil'):
    st.session_state.page = 'Perfil'

if st.session_state.page == 'Inicio':
    show_home()
if st.session_state.page == 'Perfil':
    show_perfil()