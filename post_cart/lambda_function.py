import json
import psycopg2
import os

def lambda_handler(event, context):
    status=200
    body=""
    error=""
    nombre = event.get("nombre")
    email = event.get("email")
    address = event.get("address")
    phone = event.get("phone")
    products = event.get("products")
    
    conn = psycopg2.connect(
            user=os.environ['user'],
            password=os.environ['password'],
            host=os.environ['host'],
            port=os.environ['port'],
            database=os.environ['database'])
    cursor = conn.cursor()
    
    try:
        # Inicia una transacción
        conn.autocommit = False

        # Inserta en la tabla 'buyer' y obtiene el id generado
        cursor.execute(
        """INSERT INTO public.buyer(name, email, address, phone)
    	VALUES ( %s, %s, %s, %s)
    	returning id""",
        (nombre, email,address,phone)
        )
        idBuyer = cursor.fetchone()[0]
        
        cursor.execute(
        """INSERT INTO public.carts(status, "idBuyer")
    	VALUES ( %s, %s) 
    	returning id""",
        ('pendiente',idBuyer )
        )
        idCart = cursor.fetchone()[0]

        for product in products:
            cursor.execute(
                """INSERT INTO public.product_carts(
	                product_id, cart_id, quantity) VALUES (%s, %s, %s)""",
                (product["id"],idCart, product["count"])
            )

        # Confirma la transacción
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
        body= "Servicio fallido:\n"+str(error)
        
    return {
        'statusCode': status,
        'body': body
    }
