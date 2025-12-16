import streamlit as st
import pandas as pd
from database.clientedb import obtener_todos_clientes, buscar_clientes
from datetime import datetime

def mostrar_tabla_contactos():
    st.title(" Lista de Contactos - Tabla")
    st.markdown("---")
    
    # Barra de búsqueda simple
    busqueda = st.text_input(
        " Buscar contacto", 
        placeholder="Buscar por nombre, empresa, correo..."
    )
    
    # Obtener contactos
    if busqueda:
        resultado = buscar_clientes(busqueda)
    else:
        resultado = obtener_todos_clientes()
    
    if not resultado["success"]:
        st.error(f"❌ Error al obtener contactos: {resultado['error']}")
        return
    
    contactos = resultado["data"]
    
    if not contactos:
        st.info(" No hay contactos registrados")
        return
    
    # Convertir a DataFrame
    df = pd.DataFrame(contactos)
    
    # Formatear fechas
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y')
    df['fecha_ultima_llamada'] = df['fecha_ultima_llamada'].fillna('Sin llamadas')
    
    # Rellenar valores nulos con guiones
    df = df.fillna('-')
    
    # Seleccionar columnas a mostrar
    df_mostrar = df[[
        'id',
        'nombre',
        'apellido',
        'empresa',
        'cargo',
        'correo',
        'numero_telefono',
        'veces_contactado',
        'fecha_ultima_llamada',
        'created_at'
    ]].copy()
    
    # Renombrar columnas
    df_mostrar.columns = [
        'ID',
        'Nombre',
        'Apellido',
        'Empresa',
        'Cargo',
        'Correo',
        'Teléfono',
        'Llamadas',
        'Última Llamada',
        'Fecha Registro'
    ]
    
    # Mostrar total
    st.info(f" Total de contactos: **{len(df_mostrar)}**")
    
    # Mostrar tabla
    st.dataframe(
        df_mostrar,
        use_container_width=True,
        hide_index=True,
        height=600
    )
    
    # Botón para exportar
    st.markdown("---")
    csv = df_mostrar.to_csv(index=False)
    st.download_button(
        label=" Descargar CSV",
        data=csv,
        file_name=f"contactos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )