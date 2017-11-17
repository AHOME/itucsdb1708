#from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
#from passlib.ext.django.models import password_context

class RestaurantFoods(UserMixin):
    def __init__(self, primaryId, restaurantId, foodId):
        self.primaryId = primaryId
        self.restaurantId = restaurantId
        self.foodId = foodId
