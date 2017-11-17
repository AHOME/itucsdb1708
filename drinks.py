import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin


class Drinks(Drink):
    def __init__(self, Id, name, drinkType, calorie, drinkCold ,alcohol):
        self.Id = Id
        self.name = name
        self.drinkType = drinkType
        self.calorie = calorie
        self.drinkCold = drinkCold
        self.alcohol = alcohol
