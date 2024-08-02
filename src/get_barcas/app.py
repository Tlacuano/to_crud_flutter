import json

from common.httpStatusCodeError import HttpStatusCodeError
from common.db_connection import get_db_connection

open_headers = {
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}


def lambda_handler(event, ___):
    try:
        response = get_barcas()
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


def get_barcas():
    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM barcas")
            result = cur.fetchall()
            return {
                'statusCode': 200,
                'headers': open_headers,
                'body': json.dumps(result)
            }
    except Exception as e:
        raise HttpStatusCodeError(500, str(e))
