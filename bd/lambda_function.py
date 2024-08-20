import json
from connection import Connection
from cons import Constantes
import psycopg2
import ast

def lambda_handler(event, context):
    sql = event.get("sql")
    params = event.get("params")
    function = event.get("function")
    if params:
        params = ast.literal_eval(params)
    
    data=Constantes.ERROR_SERVICIO
    def consultaGeneral(sql,parameters=''):
        msm=Constantes.PETICION_REGISTRO_VACIO
        try:
            conn = Connection.connect()
            cursor=conn.cursor()
            if parameters=='':
                cursor.execute(sql) 
            else:
                cursor.execute(sql,parameters)  
            Datos=cursor.fetchall()
            conn.commit()
            cursor.close()
            Connection.closeConnection(conn)
        except psycopg2.Error as e:
            cursor.close()
            Connection.closeConnection(conn)
            diagnostico=e.diag.severity
            mensaje=e.diag.message_primary
            msm=Constantes.ERROR_SERVICIO
            data={
                "msm":msm,
                'Response':diagnostico+': '+mensaje
                }
            return data
        serial=[]
        for j,dato in enumerate(Datos):
            response={}
            for i, value in enumerate(dato):
                response[cursor.description[i][0]]=value
            serial.append(response)
            msm=Constantes.PETICION_SERVICIO_EXITOSO
        data={"msm":msm,
            'Response':serial
            }
        return data
    
    def updateOrInsert(sql,parameters=''):
        try:    
            conn = Connection.connect()
            cursor=conn.cursor()
            if parameters=='':
                cursor.execute(sql) 
            else:
                cursor.execute(sql,parameters)  
            conn.commit()
            cursor.close()
            Connection.closeConnection(conn)
            msm=Constantes.PETICION_SERVICIO_EXITOSO
            
        except psycopg2.Error as e:
            
            cursor.close()
            Connection.closeConnection(conn)
            diagnostico= str(e.diag.severity)
            mensaje=str(e.diag.message_primary)
            msm=Constantes.ERROR_SERVICIO
            data={
                "msm":msm,
                'Response':diagnostico+': '+mensaje
                }

            return data
            
        data={"msm":msm,
              'Response':'200'
            }
        return data
        
    if function==1:
        data=consultaGeneral(sql,params)
    if function==2:
        data=updateOrInsert(sql,params)
        
    return {
        'statusCode': 200,
        'body': data
    }
