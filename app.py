import streamlit as st
from page.AgregarContacto import mostrar_formulario_agregar

st.set_page_config(page_title="CRM INNEXT")
st.write("### *Bienvenido a nuestro sistema CRM*")

st.sidebar.success("Opciones")
pagina = st.sidebar.radio("Menu CRM",["Agregar Contactos", "Contactos"])

if pagina == "Agregar Contactos":
    mostrar_formulario_agregar()



