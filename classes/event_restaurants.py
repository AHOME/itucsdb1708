#from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
#from passlib.ext.django.models import password_context

class EventRestaurants():
    def __init__(self, eventId, userId):
        self.Id = ""
        self.eventId = eventId
        self.userId = userId
        print(self.userId)
        print(self.eventId)
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO EVENT_RESTAURANTS (EVENT_ID, USER_ID)
                VALUES (%s,%s)"""
            cursor.execute(query, [self.eventId, self.userId])
            connection.commit
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM EVENT_RESTAURANTS WHERE (EVENT_ID = %s)
            AND (USER_ID = %s)"""
        cursor.execute(statement,[self.eventId, self.userId])
        IdofCurrent = cursor.fetchone()[0]
        self.Id = IdofCurrent

def select_comers_all(eventId):
    #Select name from user table who comes to that event.
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT USERS.FIRSTNAME, USERS.LASTNAME FROM EVENT_RESTAURANTS,USERS
            WHERE USERS.ID = EVENT_RESTAURANTS.USER_ID
            AND EVENT_RESTAURANTS.EVENT_ID = %s"""
        cursor.execute(statement,[eventId])
        comers = cursor.fetchall()
        return comers
def delete_comers_by_Id(eventId,userId):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            DELETE FROM EVENT_RESTAURANTS WHERE EVENT_ID = %s AND
            USER_ID = %s"""
        cursor.execute(query, [eventId,userId])
        connection.commit()
def does_user_come(userId,eventId):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM EVENT_RESTAURANTS
            WHERE USER_ID = %s
            AND EVENT_ID = %s """
        cursor.execute(statement,[userId,eventId])
        comers = cursor.fetchall()
    return comers

def delete_unnecessary_rows():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            DELETE FROM EVENT_RESTAURANTS WHERE EVENT_ID IS NULL OR
            USER_ID IS NULL"""
        cursor.execute(query)
        connection.commit()
