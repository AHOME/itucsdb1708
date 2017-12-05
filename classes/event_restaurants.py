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
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO EVENT_RESTAURANTS (EVENT_ID, USER_ID)
                VALUES (%s,%s,%s,%s,%s)"""
            cursor.execute(query, [self.eventId, self.restaurantId])
            connection.commit
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM EVENT_RESTAURANTS WHERE (EVENT_ID = %s)
            AND (USER_ID = %s)s"""
        cursor.execute(statement,[self.eventId, self.userId])
        IdofCurrent = cursor.fetchone()[0]
        self.Id = IdofCurrent
    def select_comers_all():
        #Select name from user table
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT USERS.FIRSTNAME, USERS.LASTNAME FROM EVENT_RESTAURANTS,USERS
             WHERE USERS.ID = EVENT_RESTAURANTS.USER_ID"""
            cursor.execute(statement)
            comers = cursor.fetchall()
            return comers
    def delete_comers_by_Id(Id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
                DELETE FROM EVENT_RESTAURANTS WHERE ID = %s"""
            cursor.execute(query, [Id] )
            connection.commit()
