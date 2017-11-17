#from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
#from passlib.ext.django.models import password_context

class Restaurants(UserMixin):
    def __init__(self, primaryId, name, address, contactName, contanctPhone, score, profilePicture, hours, currentStatus):
        self.primaryId = primaryId
        self.name = name
        self.address = address
        self.contactName = contactName
        self.contanctPhone = contanctPhone
        self.score = score
        self.profilePicture = profilePicture
        self.hours = hours
        self.currentStatus = currentStatus
