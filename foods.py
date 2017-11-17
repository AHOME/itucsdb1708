#from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
#from passlib.ext.django.models import password_context

class Foods(UserMixin):
    def __init__(self, primaryId, name, icon, foodType, price, calorie):
        self.primaryId = primaryId
        self.name = name
        self.icon = icon
        self.foodType = foodType
        self.price = price
        self.calori = calorie
