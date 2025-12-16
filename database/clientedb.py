from database.coneccion import getConnection
from psycopg2.extras import RealDictCursor

def registrar_cliente(nombre,apellido, empresa, cargo, correo, numero_telefono):
    try:
        conn = getConnection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = """
            INSERT INTO clientes
            (nombre, apellido, empresa, cargo, correo, numero_telefono, veces_contactado, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            RETURNING *
        """

        cursor.execute(query,(nombre, apellido, empresa, cargo, correo, numero_telefono))
        cliente = cursor.fetchone()
        conn.commit()

        cursor.close()
        conn.close()

        return{"success": True, "data":cliente}

    
    except Exception as e:
        return {"success": False, "error": str(e)}

def obtener_todos_clientes():
    try:
        conn = getConnection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = "Select * from clientes ORDER BY created_at DESC"
        cursor.execute(query)
        clientes = cursor.fetchall()
        cursor.close()
        conn.close()

        return{"success":True,"data": clientes}

    except Exception as e:
        return {"success": False, "error":str(e)}

def obtener_Cliente_ID(cliente_id):
    try:
        conn = getConnection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM clientes WHERE id=%s"
        cursor.execute(query,(cliente_id,))
        cliente = cursor.fetchone()
        cursor.close()
        conn.close()

        if cliente:
            return{"success":True, "data":cliente}
        else:
            return{"success": False,"error": "Cliente no encontrado"}
     
    except Exception as e:
        return {"success": False, "error": str(e)}

def actualizar_cliente(cliente_id, nombre, apellido, empresa, cargo, correo, numero_telefono):
    conn = getConnection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """
        UPDATE clientes 
        SET nombre = %s, apellido = %s, empresa = %s, cargo = %s, 
            correo = %s, numero_telefono = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """

    cursor.execute(query, (nombre, apellido, empresa, cargo, correo, numero_telefono, cliente_id))
    cliente = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    if cliente:
        return {"success": True, "data": cliente}   
    else:
        return{"success": False, "error": "Cliente no encontrado"} 
    
def eliminar_cliente(cliente_id):
    """Elimina un cliente de la base de datos"""
    try:
        conn = getConnection()
        cursor = conn.cursor()
        
        query = "DELETE FROM clientes WHERE id = %s"
        cursor.execute(query, (cliente_id,))
        rows_deleted = cursor.rowcount
        conn.commit()
        
        cursor.close()
        conn.close()
        
        if rows_deleted > 0:
            return {"success": True, "message": "Cliente eliminado correctamente"}
        else:
            return {"success": False, "error": "Cliente no encontrado"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def registrar_llamada(cliente_id):
    """Registra una nueva llamada a un cliente (incrementa contador y actualiza fecha)"""
    try:
        conn = getConnection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            UPDATE clientes 
            SET veces_contactado = veces_contactado + 1,
                fecha_ultima_llamada = CURRENT_DATE,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *
        """
        
        cursor.execute(query, (cliente_id,))
        cliente = cursor.fetchone()
        conn.commit()
        
        cursor.close()
        conn.close()
        
        if cliente:
            return {"success": True, "data": cliente}
        else:
            return {"success": False, "error": "Cliente no encontrado"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def buscar_clientes(termino):
    """Busca clientes por nombre, apellido, empresa o correo"""
    try:
        conn = getConnection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT * FROM clientes 
            WHERE nombre ILIKE %s 
               OR apellido ILIKE %s 
               OR empresa ILIKE %s 
               OR correo ILIKE %s
            ORDER BY created_at DESC
        """
        
        search_term = f"%{termino}%"
        cursor.execute(query, (search_term, search_term, search_term, search_term))
        clientes = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {"success": True, "data": clientes}
    
    except Exception as e:
        return {"success": False, "error": str(e)}
    


