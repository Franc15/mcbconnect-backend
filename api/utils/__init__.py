import psycopg2

def connect_to_db():
    conn = psycopg2.connect(host="localhost", database="mcbconnect-db", user="postgres", password="dhosiohoes")
    return conn