import streamlit as st
import pandas as pd
from database.clientedb import (
    obtener_todos_clientes, 
    registrar_llamada, 
    buscar_clientes,
    eliminar_cliente
)
from datetime import datetime

def mostrar_lista_contactos():
    st.title("📋 Lista de Contactos")
    
    # Barra de búsqueda
    col1, col2 = st.columns([3, 1])
    with col1:
        busqueda = st.text_input(
            "🔍 Buscar contacto", 
            placeholder="Buscar por nombre, empresa, correo...",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("🔄 Actualizar", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
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
        st.info("📭 No hay contactos registrados en el sistema")
        return
    
    # Métricas superiores
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Contactos", len(contactos))
    with col2:
        total_llamadas = sum(c['veces_contactado'] for c in contactos)
        st.metric("📞 Total Llamadas", total_llamadas)
    with col3:
        con_llamadas = sum(1 for c in contactos if c['veces_contactado'] > 0)
        st.metric("✅ Contactados", con_llamadas)
    
    st.markdown("---")
    
    # Mostrar contactos en cards
    for contacto in contactos:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### 👤 {contacto['nombre']} {contacto['apellido']}")
                if contacto['empresa']:
                    st.markdown(f"**🏢 {contacto['empresa']}**")
                if contacto['cargo']:
                    st.caption(f"💼 {contacto['cargo']}")
            
            with col2:
                if contacto['correo']:
                    st.text(f"📧 {contacto['correo']}")
                if contacto['numero_telefono']:
                    st.text(f"📞 {contacto['numero_telefono']}")
                
                if contacto['fecha_ultima_llamada']:
                    st.caption(f"📅 Última llamada: {contacto['fecha_ultima_llamada']}")
                else:
                    st.caption("📅 Sin llamadas registradas")
            
            with col3:
                st.metric(
                    "Llamadas", 
                    contacto['veces_contactado'],
                    label_visibility="visible"
                )
                
                # Botones de acción
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("📞", key=f"call_{contacto['id']}", help="Registrar llamada"):
                        registrar_llamada_accion(contacto)
                
                with btn_col2:
                    if st.button("🗑️", key=f"delete_{contacto['id']}", help="Eliminar contacto"):
                        eliminar_contacto_accion(contacto)
            
            st.markdown("---")
    
    # Opción para exportar a CSV
    if st.button("📥 Exportar a CSV"):
        df = pd.DataFrame(contactos)
        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Descargar CSV",
            data=csv,
            file_name=f"contactos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def registrar_llamada_accion(contacto):
    """Registra una llamada y muestra notificación"""
    resultado = registrar_llamada(contacto['id'])
    if resultado["success"]:
        st.success(f"✅ Llamada registrada para {contacto['nombre']} {contacto['apellido']}")
        st.rerun()
    else:
        st.error(f"❌ Error: {resultado['error']}")

def eliminar_contacto_accion(contacto):
    """Elimina un contacto con confirmación"""
    if 'confirmar_eliminar' not in st.session_state:
        st.session_state.confirmar_eliminar = {}
    
    contacto_id = contacto['id']
    
    if contacto_id not in st.session_state.confirmar_eliminar:
        st.warning(f"⚠️ ¿Está seguro de eliminar a {contacto['nombre']} {contacto['apellido']}?")
        st.session_state.confirmar_eliminar[contacto_id] = True
    else:
        resultado = eliminar_cliente(contacto_id)
        if resultado["success"]:
            st.success("✅ Contacto eliminado correctamente")
            del st.session_state.confirmar_eliminar[contacto_id]
            st.rerun()
        else:
            st.error(f"❌ Error: {resultado['error']}")
```

## 4. Estructura de archivos:
```
tu_proyecto/
├── database/
│   ├── coneccion.py
│   └── clientedb.py
├── app.py                      ← Principal (ejecuta este)
├── agregar_contacto_st.py      ← Formulario
└── listar_contactos_st.py      ← Lista