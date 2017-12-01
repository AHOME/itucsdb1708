import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context


class Events():
    #Create an object form a form.
    def __init__(self,form = None,select = None):
        if form is None:#select statement will return list object.
            self.Id = select[0]
            self.content = select[1]
            self.address = select[2]
            self.startDate = select[3]
            self.endDate = select[4]
            self.name = select[5]
            self.iconPath = select[6]
        elif select is None:
            self.Id = ""
            self.content = form['Explanations']
            self.address = form['place']
            self.startDate = form['startDate']
            self.endDate = form['endDate']
            self.name = form['Name']
            self.iconPath = ""
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """
                    INSERT INTO EVENTS (NAME, ENDINGDATE, CONTENT, ADDRESS, STARTINGDATE)
                    VALUES (%s,%s,%s,%s,%s)"""
                cursor.execute(query, (self.name, self.endDate, self.content, self.address, self.startDate))
                connection.commit()
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT * FROM EVENTS WHERE (NAME = %s)
                AND (ENDINGDATE = %s)
                AND (CONTENT = %s)
                AND (ADDRESS = %s)
                AND (STARTINGDATE = %s)"""
                cursor.execute(statement,[self.name,self.endDate, self.content, self.address, self.startDate])
                IdofCurrent = cursor.fetchone()[0]
                self.Id = IdofCurrent
