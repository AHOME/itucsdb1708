#from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
#from passlib.ext.django.models import password_context

"""class Achievements():
    def __init__(self, primaryId, icon, content, name):
        self.primaryId = primaryId
        self.name = name
        self.icon = icon
        self.content = content"""

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
            self.icon = ""
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
