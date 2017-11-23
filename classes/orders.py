#from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
#from passlib.ext.django.models import password_context

class Orders():
    def __init__(self, primaryId, userId, restaurantId, price, date, status):
        self.primaryId = primaryId
        self.userId = userId
        self.restaurantId = restaurantId
        self.price = price
        self.date = date
        self.status = status
