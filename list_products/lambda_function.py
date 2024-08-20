import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('lambda', region_name="us-east-2", )
    sql="""SELECT id, nombre, sku, descripcion, image, price
	        FROM public.products; """
    payload =  {
            "sql": sql,
            "params": "",
            "function": 1
        }
    response = client.invoke(
            FunctionName="bd",
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
    out_lambda=json.loads(response['Payload'].read().decode('utf-8'))
    
    return  out_lambda
    
