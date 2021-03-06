#from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context


class Achievements():
    def __init__(self,form = None,select = None):
        if form is None:
            self.Id = select[0]
            self.name = select[1]
            self.icon = select[2]
            self.content = select[3]
            self.goal = select[4]
            self.endDate = select[5]
        elif select is None:
            self.Id = ""
            self.name = form['Name']
            self.icon = form['Icon']
            self.content = form['Explanation']
            self.goal = form['Goal']
            self.endDate = form['endDate']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """
                    INSERT INTO ACHIEVEMENTS (NAME, ICON, CONTENT, GOAL, ENDDATE)
                    VALUES (%s,%s,%s,%s,%s)"""
                cursor.execute(query, (self.name, self.icon, self.content, self.goal, self.endDate))
                connection.commit()
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT * FROM ACHIEVEMENTS WHERE (NAME = %s)
                AND (ICON = %s)
                AND (CONTENT = %s)
                AND (GOAL = %s)
                AND (ENDDATE = %s)"""
                cursor.execute(statement,[self.name,self.icon, self.content, self.goal, self.endDate])
                IdofCurrent = cursor.fetchone()[0]
                self.Id = IdofCurrent


def achievement_update(form, achievement_id):
    name = form['Name']
    content = form['Explanation']
    goal = form['Goal']
    endDate = form['endDate']
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """UPDATE ACHIEVEMENTS SET NAME=%s, CONTENT=%s, GOAL=%s, ENDDATE=%s  WHERE (ID = %s)"""
        cursor.execute(statement,[name, content, goal, endDate, achievement_id])
        connection.commit()

def achievement_select_by_Id(Id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM ACHIEVEMENTS WHERE (ID = %s)"""
        cursor.execute(statement,[Id])
        return cursor.fetchone()

def achievement_delete_by_Id(Id):
    query = """DELETE FROM ACHIEVEMENTS WHERE ID = %s"""
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        cursor.execute(query, [Id])
        connection.commit()

def achievement_select_all():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM ACHIEVEMENTS"""
        cursor.execute(query)
        return cursor.fetchall()
