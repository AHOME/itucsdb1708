import psycopg2 as dbapi2
from flask import current_app

def select_all_messages():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM MESSSAGES"""
        cursor.execute(statement)
        messages = cursor.fetchall()
        
        return messages