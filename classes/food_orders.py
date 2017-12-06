import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
import datetime

class FoodOrders():
    def __init__(self):
        self.primaryId = ""
        self.userId = ""
        self.restaurantId = ""
        self.foodId = ""
        self.price = ""
        self.date = ""
        self.status = ""

    def create_foodOrders(self,restaurant_id, user_id, food, price):
        self.primaryId = 0
        self.userId = user_id
        self.restaurantId = restaurant_id
        self.foodId = food
        self.price = price
        self.date = datetime.datetime.now()
        self.status = "Not Recieved"
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO FOOD_ORDERS (USER_ID, REST_ID, FOOD_ID, PRICE, BUYDATE, STATUS)
                VALUES (%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, [self.userId, self.restaurantId, self.foodId, self.price,self.date,self.status])
            connection.commit()
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE RESTAURANT_FOODS SET SELL_COUNT = SELL_COUNT + 1 WHERE RESTAURANT_ID = %s AND FOOD_ID = %s"""
            cursor.execute(query, [self.restaurantId, self.foodId])
            connection.commit()
