import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context


class Events():
    def __init__(self, Id, content, address, startDate, endDate ,name, iconPath):
        self.Id = Id
        self.content = content
        self.address = address
        self.startDate = startDate
        self.endDate = endDate
        self.name = name
        self.iconPath = iconPath
