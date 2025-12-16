import streamlit as st
from page.AgregarContacto import mostrar_formulario_agregar
from page.listarContacto import mostrar_lista_contactos
from page.listarContactoTabla import mostrar_tabla_contactos

st.set_page_config(page_title="CRM INNEXT")
st.write("### *Bienvenido a nuestro sistema CRM*")

st.sidebar.success("Opciones")
pagina = st.sidebar.radio("Menu CRM",["Agregar Contactos", "Contactos","Listar Contactos"])

if pagina == "Agregar Contactos":
    mostrar_formulario_agregar()
elif pagina == "Contactos":
    mostrar_lista_contactos()
elif pagina == "Listar Contactos":
    mostrar_tabla_contactos()




