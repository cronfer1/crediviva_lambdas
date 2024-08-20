import json
import psycopg2
import os

def lambda_handler(event, context):
    status=200
    body=""
    error=""
    id = event.get("id")
    conn = psycopg2.connect(
            user=os.environ['user'],
            password=os.environ['password'],
            host=os.environ['host'],
            port=os.environ['port'],
            database=os.environ['database'])
    cursor = conn.cursor()
    
    try:
        # Inserta en la tabla 'buyer' y obtiene el id generado
        cursor.execute(
        """UPDATE public.carts
        	set status='completado'
        	WHERE id=%s; """,
        (id,)
        )
        conn.commit()
        print("Datos insertados correctamente")

    except Exception as e:
        status=400
        error=e
        conn.rollback()
        print(f"Error al insertar datos: {e}")

    finally:
        # Cierra el cursor y la conexión
        cursor.close()
        conn.close()
        
    if status==200:
        body= "Servicio exitoso"
    else:
        body= "Servicio fallido: "+str(error)
        
    return {
        'statusCode': status,
        'body': body,
    }
