import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context

class DrinkOrders():
    def __init__(self):
        self.primaryId = ""
        self.userId = ""
        self.restaurantId = ""
        self.drinkId = ""
        self.price = ""
        self.date = ""
        self.status = ""

    def create_drinkOrders(self,restaurant_id, user_id, drink, price):
        self.primaryId = 0
        self.userId = user_id
        self.restaurantId = restaurant_id
        self.drinkId = drink
        self.price = price
        self.date = now.date().isoformat()
        self.status = "Not Recieved"
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO DRINK_ORDERS (USER_ID, REST_ID, drink_ID, PRICE, BUYDATE, STATUS)
                VALUES (%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, [self.user_id, self.restaurant_id, self.drink_id, self.price,self.date,self.status])
            connection.commit()
