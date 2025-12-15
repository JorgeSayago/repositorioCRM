import streamlit as st
from database.clientedb import registrar_cliente

def mostrar_formulario_agregar():
    st.title("📝 Agregar Nuevo Contacto")
    st.markdown("---")
    
    # Crear formulario
    with st.form("form_agregar_contacto", clear_on_submit=True):
        st.subheader("Información del Contacto")
        
        # Crear dos columnas para mejor layout
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input(
                "Nombre *", 
                placeholder="Ej: Juan",
                help="Campo obligatorio"
            )
            empresa = st.text_input(
                "Empresa", 
                placeholder="Ej: Tech Solutions"
            )
            correo = st.text_input(
                "Correo Electrónico", 
                placeholder="Ej: juan@empresa.com"
            )
        
        with col2:
            apellido = st.text_input(
                "Apellido *", 
                placeholder="Ej: Pérez",
                help="Campo obligatorio"
            )
            cargo = st.text_input(
                "Cargo", 
                placeholder="Ej: Gerente de Compras"
            )
            numero_telefono = st.text_input(
                "Número de Teléfono", 
                placeholder="Ej: +593987654321"
            )
        
        st.markdown("---")
        st.caption("* Campos obligatorios")
        
        # Botón de envío
        submitted = st.form_submit_button(
            "✅ Guardar Contacto",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            # Validaciones
            if not nombre or not apellido:
                st.error("❌ El nombre y apellido son obligatorios")
                return
            
            if not correo and not numero_telefono:
                st.error("❌ Debe proporcionar al menos un correo o teléfono")
                return
            
            # Intentar registrar
            with st.spinner("Guardando contacto..."):
                resultado = registrar_cliente(
                    nombre=nombre.strip(),
                    apellido=apellido.strip(),
                    empresa=empresa.strip() if empresa else None,
                    cargo=cargo.strip() if cargo else None,
                    correo=correo.strip() if correo else None,
                    numero_telefono=numero_telefono.strip() if numero_telefono else None
                )
            
            if resultado["success"]:
                st.success(f"✅ Contacto registrado exitosamente! ID: {resultado['data']['id']}")
                st.balloons()
            else:
                st.error(f"❌ Error al registrar: {resultado['error']}")
    
    # Mostrar preview de datos
    st.markdown("---")
    with st.expander("ℹ️ Información sobre los campos"):
        st.markdown("""
        - **Nombre y Apellido**: Identificación del contacto
        - **Empresa**: Organización a la que pertenece
        - **Cargo**: Posición en la empresa
        - **Correo**: Email de contacto
        - **Teléfono**: Número telefónico (incluir código de país)
        """)