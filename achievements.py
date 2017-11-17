#from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
#from passlib.ext.django.models import password_context

class Achievements(UserMixin):
    def __init__(self, primaryId, icon, content, name):
        self.primaryId = primaryId
        self.name = name
        self.icon = icon
        self.content = content
