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
    


