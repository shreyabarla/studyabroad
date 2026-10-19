import psycopg2

def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="altiora_db",
        user="postgres",
        password="Chamuchene"      
    )

    return connection