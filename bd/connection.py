import psycopg2
import os 
class Connection:

    def connect():
        try:
            connection = psycopg2.connect(
            user=os.environ['user'],
            password=os.environ['password'],
            host=os.environ['host'],
            port=os.environ['port'],
            database=os.environ['database'])
            return connection
        except psycopg2.Error as e:
            diagnostico=e.diag.severity
            mensaje=e.diag.message_primary
            print(diagnostico ,mensaje)
            return diagnostico+mensaje

    def closeConnection( connection):
        connection.close()
    
