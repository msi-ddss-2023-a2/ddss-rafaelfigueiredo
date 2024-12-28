import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5433,  # Altere para 5432 se necessário
        database="auth_db",
        user="user123",
        password="user123",
    )
