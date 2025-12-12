import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extras import Json

def getConnection():
    return psycopg2.connect(
        dbname="crm_bd",
        user="postgres",
        password="admin",
        host="localhost"
    )