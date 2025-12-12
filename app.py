import streamlit as st

st.set_page_config(page_title="CRM INNEXT")
st.write("### *Bienvenido a nuestro sistema CRM*")

st.sidebar.success("Opciones")
pagina = st.sidebar.radio("Menu CRM",["Agregar Contactos", "Contactos"])



