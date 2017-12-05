#from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
#from passlib.ext.django.models import password_context

class Foods():
    def __init__(self):
        self.primaryId = ""
        self.name = ""
        self.icon = ""
        self.foodType = ""
        self.price = ""
        self.calori = ""

    def select_all_foods(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM FOODS"""
            cursor.execute(query)
            foods = cursor.fetchall()
        return foods

    def create_food(self, form):

        nameInput = form['name']
        iconInput = form['icon']
        typeNameInput = form['type']
        priceInput = form['price']
        calorieInput = form['calorie']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO FOODS (NAME, ICON, FOOD_TYPE, PRICE, CALORIE)
                VALUES (%s,%s,%s,%s,%s)"""
            cursor.execute(query, [nameInput, iconInput, typeNameInput, priceInput, calorieInput])
            connection.commit()
