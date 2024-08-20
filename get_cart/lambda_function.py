import json
import psycopg2
import boto3
import os

client = boto3.client('lambda', region_name="us-east-2" )

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
    
    sql="""SELECT a.id,b.email,json_agg(json_build_object('nombre', d.nombre, 'quantity', c.quantity,'price',d.price)) AS product_details,
	status,sum(d.price * c.quantity) as total_price, TO_CHAR(a.created, 'YYYY-MM-DD') as created
	FROM public.carts as a	
	join public.buyer as b on a."idBuyer"=b.id
	join public.product_carts as c on a.id=c.cart_id
	join public.products as d on d.id=c.product_id
	group by  a.id,email, status,a.created
	order by status desc, created asc; """
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        datos = cursor.fetchall()
    except (Exception, psycopg2.Error) as e:
        print("Error al consultar la base de datos", e)
        error=e
    finally:
        cursor.close()
        conn.close()
            
    if status==200:
        serial=[]
        for j,dato in enumerate(datos):
            response={}
            for i, value in enumerate(dato):
                response[cursor.description[i][0]]=value
            serial.append(response)
        body= serial
    else:
        body= "Servicio fallido:\n"+str(error)
    print(body)
    # json.loads(resultados.read().decode('utf-8')
    return {
        'statusCode': status,
        'body': body
    }
