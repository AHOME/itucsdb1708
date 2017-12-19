import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
import datetime

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
        self.date = datetime.datetime.now()
        self.status = "Not Recieved"
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO DRINK_ORDERS (USER_ID, REST_ID, drink_ID, PRICE, BUYDATE, STATUS)
                VALUES (%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, [self.userId, self.restaurantId, self.drinkId, self.price,self.date,self.status])
            connection.commit()

def select_drink_oders_user_notReceived(userID):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT RESTAURANTS.NAME,DRINKS.NAME,DRINK_ORDERS.PRICE,BUYDATE,STATUS,RESTAURANTS.ID,DRINK_ORDERS.ID
        FROM DRINK_ORDERS,RESTAURANTS,DRINKS WHERE USER_ID = %s AND
        DRINK_ORDERS.REST_ID = RESTAURANTS.ID AND DRINKS.ID = DRINK_ORDERS.DRINK_ID AND DRINK_ORDERS.STATUS = %s"""
        cursor.execute(query, [userID,"Not Recieved"])
        return cursor.fetchall()

def select_drink_oders_user_Received(userID):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT RESTAURANTS.NAME,DRINKS.NAME,DRINK_ORDERS.PRICE,BUYDATE,STATUS,RESTAURANTS.ID,DRINK_ORDERS.ID
         FROM DRINK_ORDERS,RESTAURANTS,DRINKS WHERE USER_ID = %s AND
        DRINK_ORDERS.REST_ID = RESTAURANTS.ID AND DRINKS.ID = DRINK_ORDERS.DRINK_ID AND DRINK_ORDERS.STATUS = %s"""
        cursor.execute(query, [userID,"Received"])
        return cursor.fetchall()

def delete_drink_order_by_id(orderId):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            DELETE FROM DRINK_ORDERS WHERE ID = %s"""
        cursor.execute(query, [orderId] )
        connection.commit()

def update_drink_order_by_id(orderId):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """
        UPDATE DRINK_ORDERS SET
        STATUS = %s
        WHERE (ID = %s)"""
        cursor.execute(statement,["Received",orderId])
        connection.commit()
