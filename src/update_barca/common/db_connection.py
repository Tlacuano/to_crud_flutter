import pymysql
from httpStatusCodeError import HttpStatusCodeError

DB_HOST = 'database-1.cl0i4sksgakv.us-east-2.rds.amazonaws.com'
DB_NAME = 'barca'
USERNAME = 'admin'
PASSWORD = 'admin123'


def get_db_connection():
    host = DB_HOST
    user = USERNAME
    password = PASSWORD
    db_name = DB_NAME

    try:
        return pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db_name
        )
    except pymysql.MySQLError:
        raise HttpStatusCodeError(500, "Error connecting to database")


