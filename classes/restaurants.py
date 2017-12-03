import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
import datetime
#from passlib.ext.django.models import password_context

class Restaurant():
    def __init__(self,):
        self.primaryId = ""
        self.name =  ""
        self.address = ""
        self.contactName = ""
        self.contactPhone =  ""
        self.score = 0
        self.profilePicture = ""
        self.hours = ""
        self.currentStatus = ""

    def create_restaurant(self, form):

        self.primaryId = ""
        self.name =  form['Name']
        self.address = form['Address']
        self.contactName = form['ContactName']
        self.contactPhone = form['ContactPhone']
        self.score = 0
        self.profilePicture = form['Photo']
        self.hours = form['WorkingHours']
        self.currentStatus = form['CurrentStatus']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RESTAURANTS (NAME, ADDRESS, CONTACT_NAME, CONTACT_PHONE, PROFILE_PICTURE, HOURS, CURRENT_STATUS)
                VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, [self.name, self.address, self.contactName, self.contactPhone, self.profilePicture, self.hours, self.currentStatus])
            connection.commit()

    def select_all_restaurants(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM RESTAURANTS"""
            cursor.execute(query)
            restaurants = cursor.fetchall()
        return restaurants


    def select_restaurant_by_id(self, r_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM RESTAURANTS WHERE id = %s"""
            cursor.execute(query, [r_id])
            value = cursor.fetchall()
            selectedRestaurant = value[0]
            self.primaryId  =  selectedRestaurant[0]
            self.name =  selectedRestaurant[1]
            self.address =  selectedRestaurant[2]
            self.contactName =  selectedRestaurant[3]
            self.contactPhone =  selectedRestaurant[4]
            self.score =  selectedRestaurant[5]
            self.profilePicture =  selectedRestaurant[6]
            self.hours =  selectedRestaurant[7]
            self.currentStatus =  selectedRestaurant[8]


    def delete_restaurant_by_id(self, r_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM RESTAURANTS WHERE ID = %s"""
            cursor.execute(query, [r_id])
            connection.commit()

    def update_restaurant_by_id(self, form, restaurantId):
        self.primaryId = restaurantId
        self.name =  form['Name']
        self.address = form['Address']
        self.contactName = form['contactName']
        self.contactPhone =  form['contactPhone']
        self.score = 0
        self.profilePicture = form['Photo']
        self.hours = form['WorkingHours']
        self.currentStatus = form['CurrentStatus']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE RESTAURANTS SET NAME = %s, ADDRESS = %s, CONTACT_NAME = %s, CONTACT_PHONE = %s, PROFILE_PICTURE = %s, HOURS = %s, CURRENT_STATUS = %s WHERE ID = %s"""
            cursor.execute(query, [self.name, self.address, self.contactName, self.contactPhone, self.profilePicture, self.hours, self.currentStatus, self.primaryId])
            connection.commit()

    def create_comment(self, form):
        content = form['comment']
        restaurantId = form['restaurant_id']
        userId = form['user_id']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO COMMENTS (USER_ID, RESTAURANT_ID, CONTENT, SENDDATE)
                VALUES (%s,%s,%s,%s)"""
            cursor.execute(query, [int(userId), int(restaurantId), content, datetime.datetime.now()])
            connection.commit()

    def select_all_comments(self, restaurantId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM COMMENTS AS x JOIN USERS AS y ON x.USER_ID = y.ID WHERE RESTAURANT_ID = %s"""
            cursor.execute(query, [restaurantId])
            comments = cursor.fetchall()
        return comments

    def delete_comment_by_id(self, c_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM COMMENTS WHERE ID = %s"""
            cursor.execute(query, [c_id])
            connection.commit()
