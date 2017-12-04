#from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
#from passlib.ext.django.models import password_context

class Deals():
    def __init__(self, select=None, form=None, foodId=None, restaurantId=None):
        if form is None:
            self.primaryId = select[0]
            self.foodId = select[1]
            self.restaurantId = select[2]
            self.date = select[3]
            self.discountRate = select[4]
        else:
            self.foodId = foodId
            self.restaurantId = restaurantId
            self.date = form['ValidDate']
            self.discountRate = form['rate']

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO DEALS (FOOD_ID, REST_ID, DATE, DISCOUNT_RATE)
                VALUES (%s,%s,%s,%s)"""
            cursor.execute(query, [self.foodId, self.restaurantId, self.date, self.discountRate])
            connection.commit()
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM DEALS WHERE (FOOD_ID = %s)
            AND (REST_ID = %s)
            AND (DATE = %s)
            AND (DISCOUNT_RATE = %s)"""
            cursor.execute(statement,[self.foodId, self.restaurantId, self.date, self.discountRate])
            IdofCurrent = cursor.fetchone()[0]
            self.primaryId = IdofCurrent
