from server import app
import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
#from passlib.ext.django.models import password_context

class Restaurants():
    def __init__(self,):
        self.primaryId = ""
        self.name =  ""
        self.address = ""
        self.contactName = ""
        self.contanctPhone =  ""
        self.score = 0
        self.profilePicture = ""
        self.hours = ""
        self.currentStatus = ""

    def create_restaurant(form):
        self.primaryId = ""
        self.name =  form['Name']
        self.address = form['Address']
        self.contactName = form['ContanctName']
        self.contanctPhone =  form['ContanctPhone']
        self.score = 0
        self.profilePicture = form['Photo']
        self.hours = form['WorkingHours']
        self.currentStatus = form['CurrentStatus']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO RESTAURANTS (NAME, ADDRESS, CONTACT_NAME, CONTACT_PHONE, PROFILE_PICTURE, HOURS, CURRENT_STATUS)
                VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, [self.name , self.address, self.contactName, self.contanctPhone, self.profilePicture, self.hours, self.currentStatus ])
            connection.commit()

    def select_all_restaurants():
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM RESTAURANTS"""
            cursor.execute(query)
            restaurants = cursor.fetchall()
        return restaurants


    def select_restaurant_by_id(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM RESTAURANTS WHERE id = %s"""
            cursor.execute(query, [restaurant_id])
            value = cursor.fetchall()
            selectedRestaurant = value[0]
            self.primaryId  =  selectedRestaurant[10
            self.name =  selectedRestaurant[1]
            self.address =  selectedRestaurant[2]
            self.contactName =  selectedRestaurant[3]
            self.contanctPhone =  selectedRestaurant[4]
            self.score =  selectedRestaurant[5]
            self.profilePicture =  selectedRestaurant[6]
            self.hours =  selectedRestaurant[7]
            self.currentStatus =  selectedRestaurant[8]


    # def delete_restaurant_by_id(Id):
    #     with dbapi2.connect(current_app.config['dsn']) as connection:
    #         cursor = connection.cursor()
    #         query = """DELETE FROM RESTAURANTS WHERE ID = %s"""
    #         cursor.execute(query, [restaurant_id])
    #         connection.commit()
    #
    # def update_restaurant_by_id(form,restaurantId):
    #     nameInput =  form['Name']
    #     addressInput =  form['Address']
    #     contactNameInput =  form['ContanctName']
    #     contactPhoneInput =  form['ContanctPhone']
    #     photoInput =  form['Photo']
    #     workingHoursInput =  form['WorkingHours']
    #     currentStatusInput =  form['CurrentStatus']
    #     with dbapi2.connect(current_app.config['dsn']) as connection:
    #         cursor = connection.cursor()
    #         query = """UPDATE RESTAURANTS SET NAME = %s, ADDRESS = %s, CONTACT_NAME = %s, CONTACT_PHONE = %s, PROFILE_PICTURE = %s, HOURS = %s, CURRENT_STATUS = %s WHERE ID = %s"""
    #         cursor.execute(query, [nameInput, addressInput, contactNameInput, contactPhoneInput, photoInput, workingHoursInput, currentStatusInput, restaurant_id])
    #         connection.commit()







# def select_all_restaurants():
#     with dbapi2.connect(current_app.config['dsn']) as connection:
#         cursor = connection.cursor()
#         query = """SELECT * FROM RESTAURANTS"""
#         cursor.execute(query)
#         restaurants = cursor.fetchall()
#     return restaurants
#
#
# def select_restaurant_by_id(id):
#     with dbapi2.connect(current_app.config['dsn']) as connection:
#         cursor = connection.cursor()
#         query = """SELECT * FROM RESTAURANTS WHERE id = %s"""
#         cursor.execute(query, [restaurant_id])
#         value = cursor.fetchall()
#         selectedRestaurant = value[0]
#     return selectedRestaurant
#
#
# def delete_restaurant_by_id(Id):
#     with dbapi2.connect(current_app.config['dsn']) as connection:
#         cursor = connection.cursor()
#         query = """DELETE FROM RESTAURANTS WHERE ID = %s"""
#         cursor.execute(query, [restaurant_id])
#         connection.commit()
#
#
#   def update_restaurant_by_id(form,restaurantId):
#         nameInput =  form['Name']
#         addressInput =  form['Address']
#         contactNameInput =  form['ContanctName']
#         contactPhoneInput =  form['ContanctPhone']
#         photoInput =  form['Photo']
#         workingHoursInput =  form['WorkingHours']
#         currentStatusInput =  form['CurrentStatus']
#         with dbapi2.connect(current_app.config['dsn']) as connection:
#             cursor = connection.cursor()
#             query = """UPDATE RESTAURANTS SET NAME = %s, ADDRESS = %s, CONTACT_NAME = %s, CONTACT_PHONE = %s, PROFILE_PICTURE = %s, HOURS = %s, CURRENT_STATUS = %s WHERE ID = %s"""
#             cursor.execute(query, [nameInput, addressInput, contactNameInput, contactPhoneInput, photoInput, workingHoursInput, currentStatusInput, restaurant_id])
#             connection.commit()
#
#
#
#  def __init__(self, form = None,select  = None):
#           if select is None:
#               self.Id = ""
#               self.name = form['Name']
#               self.calorie = form['calorie']
#               self.drinkCold =form['drink_cold']
#               self.alcohol = form['alcohol']
#               self.drinkType = form['Soda']
#               with dbapi2.connect(current_app.config['dsn']) as connection:
#                   cursor = connection.cursor()
#                   query = """
#                       INSERT INTO DRINKS (NAME, TYPE, CALORIE, DRINKCOLD, ALCOHOL)
#                       VALUES (%s,%s,%s,%s,%s)"""
#                   cursor.execute(query, [self.name, self.drinkType, self.calorie, self.drinkCold, self.alcohol])
#                   connection.commit()
#               with dbapi2.connect(current_app.config['dsn']) as connection:
#                   cursor = connection.cursor()
#                   statement = """SELECT * FROM DRINKS WHERE (ALCOHOL = %s)
#                   AND (NAME = %s)
#                   AND (TYPE = %s)
#                   AND (CALORIE = %s)
#                   AND (DRINKCOLD = %s)"""
#                   cursor.execute(statement,[self.alcohol, self.name, self.drinkType, self.calorie, self.drinkCold])
#                   IdofCurrent = cursor.fetchone()[0]
#                   self.Id = IdofCurrent
#           elif form is None:
#               self.Id = select[0]
#               self.name = select[1]
#               self.calorie = select[3]
#               self.drinkCold = select[4]
#               self.alcohol = select[5]
#               self.drinkType = select[2]
