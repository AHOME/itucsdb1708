#from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
#from passlib.ext.django.models import password_context

class Deals(UserMixin):
    def __init__(self, primaryId, foodId, restaurantId, date, discountRate):
        self.primaryId = primaryId
        self.foodId = foodId
        self.restaurantId = restaurantId
        self.date = date
        self.discountRate = discountRate
