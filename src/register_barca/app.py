import json
import pymysql

# Configuración de la base de datos
DB_HOST = 'database-1.cl0i4sksgakv.us-east-2.rds.amazonaws.com'
DB_NAME = 'barca'
USERNAME = 'admin'
PASSWORD = 'admin123'

def get_db_connection():
    """Función para obtener la conexión a la base de datos."""
    try:
        return pymysql.connect(
            host=DB_HOST,
            user=USERNAME,
            password=PASSWORD,
            db=DB_NAME
        )
    except pymysql.MySQLError:
        raise HttpStatusCodeError(500, "Error connecting to database")

class HttpStatusCodeError(Exception):
    """ Excepción personalizada para manejar errores de código de estado HTTP.

    Args:
        status_code (int): Código de estado HTTP
        message (str): Mensaje de error

    Attributes:
        status_code (int): Código de estado HTTP
        message (str): Mensaje de error
    """
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

# Configuración de CORS
open_headers = {
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}

def lambda_handler(event, ___):
    """Manejador Lambda para procesar los eventos."""
    try:
        body = json.loads(event['body'])
        response = register_barca(body)
    except HttpStatusCodeError as e:
        response = {
            'statusCode': e.status_code,
            'headers': open_headers,
            'body': json.dumps(e.message)
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'headers': open_headers,
            'body': json.dumps(f"An error occurred: {str(e)}")
        }

    return response

def register_barca(body):
    """Función para registrar una nueva barca en la base de datos."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO barcas (nombre, tipo, longitud, capacidad) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (body['nombre'], body['tipo'], body['longitud'], body['capacidad']))
            conn.commit()
            return {
                'statusCode': 200,
                'headers': open_headers,
                'body': json.dumps("Barca registered successfully")
            }
    except Exception as e:
        raise HttpStatusCodeError(500, str(e))

