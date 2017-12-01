import psycopg2 as dbapi2
from flask import current_app

def select_all_drinks():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM DRINKS"""
        cursor.execute(statement)
        drinks = cursor.fetchall()
        return drinks

#Return list that database returns
def select_drink_by_id(Id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM DRINKS WHERE (ID = %s)"""
        cursor.execute(statement,[Id])
        return cursor.fetchone()

def delete_drink_by_id(Id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            DELETE FROM DRINKS WHERE ID = %s"""
        cursor.execute(query, [Id] )
        connection.commit()

def update_drink_by_id(form,drinkId):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """
        UPDATE DRINKS SET NAME = %s,
        TYPE = %s,
        CALORIE = %s,
        DRINKCOLD = %s,
        ALCOHOL = %s
        WHERE (ID = %s)"""
        cursor.execute(statement,[form['Name'],form['Soda'],form['calorie'], form['drink_cold'],form['alcohol'], drinkId])
        connection.commit()
