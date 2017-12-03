import psycopg2 as dbapi2
from flask import current_app

def select_all_events():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM EVENTS"""
        cursor.execute(statement)
        events = cursor.fetchall()
        return events

#Return list that database returns
def select_event_by_id(Id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM EVENTS WHERE (ID = %s)"""
        cursor.execute(statement,[Id])
        return cursor.fetchone()

def delete_event_by_id(Id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            DELETE FROM EVENTS WHERE ID = %s"""
        cursor.execute(query, [Id] )
        connection.commit()

def update_event_by_id(form,eventId):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """
        UPDATE EVENTS SET NAME = %s,
        ENDINGDATE = %s,
        CONTENT = %s,
        ADDRESS = %s,
        STARTINGDATE = %s
        WHERE (ID = %s)"""
        cursor.execute(statement,[form['Name'],form['endDate'],form['Explanations'], form['place'],form['startDate'], eventId])
        connection.commit()
