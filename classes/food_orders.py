import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
import datetime
from classes.achievement_user import add_row

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
        #Check if any deal for that food present.
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT DISCOUNT_RATE FROM DEALS WHERE (FOOD_ID = %s) AND (REST_ID = %s)"""
            cursor.execute(query, [self.foodId,self.restaurantId])
            deal_info = cursor.fetchone()
        if deal_info:
            self.price = str( float(self.price) - float(deal_info[0]) * float(self.price) / 100.0)
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

def select_food_oders_user_notReceived(userID):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT RESTAURANTS.NAME,FOODS.NAME,FOOD_ORDERS.PRICE,BUYDATE,STATUS,RESTAURANTS.ID,FOOD_ORDERS.ID FROM FOOD_ORDERS,RESTAURANTS,FOODS WHERE USER_ID = %s AND
        FOOD_ORDERS.REST_ID = RESTAURANTS.ID AND FOODS.ID = FOOD_ORDERS.FOOD_ID AND FOOD_ORDERS.STATUS = %s"""
        cursor.execute(query, [userID,"Not Recieved"])
        return cursor.fetchall()
def select_food_oders_user_Received(userID):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT RESTAURANTS.NAME,FOODS.NAME,FOOD_ORDERS.PRICE,BUYDATE,STATUS,RESTAURANTS.ID,FOOD_ORDERS.ID FROM FOOD_ORDERS,RESTAURANTS,FOODS WHERE USER_ID = %s AND
        FOOD_ORDERS.REST_ID = RESTAURANTS.ID AND FOODS.ID = FOOD_ORDERS.FOOD_ID AND FOOD_ORDERS.STATUS = %s"""
        cursor.execute(query, [userID,"Received"])
        return cursor.fetchall()

def delete_food_order_by_id(orderId):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            DELETE FROM FOOD_ORDERS WHERE ID = %s"""
        cursor.execute(query, [orderId] )
        connection.commit()
def update_food_order_by_id(orderId,user_id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """
        UPDATE FOOD_ORDERS SET
        STATUS = %s
        WHERE (ID = %s)"""
        cursor.execute(statement,["Received",orderId])
        connection.commit()
    #Find food from its table to update achievements.
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT FOODS.NAME,FOODS.FOOD_TYPE,FOODS.CALORIE FROM FOODS,FOOD_ORDERS WHERE (FOOD_ORDERS.ID = %s)
        AND (FOODS.ID = FOOD_ID) """
        cursor.execute(query, [orderId])
        food_info = cursor.fetchone()
        add_row(user_id,1) #First order achievement.
        if food_info[1] == "Meat": #Eat meat achievement.
            add_row(user_id,2)
        if int(food_info[2]) < 100:#Eat healthy achievement.
            add_row(user_id,3)
