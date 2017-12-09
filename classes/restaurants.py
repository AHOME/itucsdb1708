import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
import datetime
#from passlib.ext.django.models import password_context

class Restaurant():
    def __init__(self):
        self.primaryId = ""
        self.name =  ""
        self.address = ""
        self.contactName = ''
        self.creatorId =  ""
        self.score = 0
        self.profilePicture = ""
        self.hours = ""
        self.currentStatus = ""

    def create_restaurant(self, form, current_user_id):
        self.primaryId = ""
        self.name =  form['Name']
        self.address = form['Address']
        self.contactName = form['ContactName']
        self.creatorId = current_user_id
        self.score = 0
        self.profilePicture = form['Photo']
        self.hours = form['WorkingHours']
        self.currentStatus = form['CurrentStatus']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RESTAURANTS (NAME, ADDRESS, CONTACT_NAME, CREATOR_ID, PROFILE_PICTURE, HOURS, CURRENT_STATUS)
                VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, [self.name, self.address, self.contactName,current_user_id , self.profilePicture, self.hours, self.currentStatus])
            connection.commit()
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT ID FROM RESTAURANTS WHERE (NAME = %s) AND  (ADDRESS = %s) AND (CONTACT_NAME = %s)
            AND (CREATOR_ID = %s) AND (PROFILE_PICTURE = %s) AND (HOURS = %s) AND (CURRENT_STATUS = %s) """
            cursor.execute(query, [self.name, self.address, self.contactName,current_user_id , self.profilePicture, self.hours, self.currentStatus])
            self.primaryId = cursor.fetchone()[0]

    def create_restaurant_with_attributes(self, id, name, address, contactName, creatorId, score, profilePic, hours, currentStatus):
        self.primaryId = id
        self.name = name
        self.address = address
        self.contactName = contactName
        self.creatorId = creatorId
        self.score = score
        self.profilePicture = profilePic
        self.hours = hours
        self.currentStatus = currentStatus


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
            if not value:
                selectedRestaurant = value[0]
                self.primaryId  =  selectedRestaurant[0]
                self.name =  selectedRestaurant[1]
                self.address =  selectedRestaurant[2]
                self.contactName =  selectedRestaurant[4]
                self.creatorId =  selectedRestaurant[3]
                self.score =  selectedRestaurant[5]
                self.profilePicture =  selectedRestaurant[6]
                self.hours =  selectedRestaurant[7]
                self.currentStatus =  selectedRestaurant[8]
            else:
                selectedRestaurant = value[0]
                self.primaryId  =  selectedRestaurant[0]
                self.name =  selectedRestaurant[1]
                self.address =  selectedRestaurant[2]
                self.contactName =  selectedRestaurant[4]
                self.creatorId =  selectedRestaurant[3]
                self.score =  selectedRestaurant[5]
                self.profilePicture =  selectedRestaurant[6]
                self.hours =  selectedRestaurant[7]
                self.currentStatus =  selectedRestaurant[8]
                return None

    def delete_restaurant_by_id(self, r_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM RESTAURANTS WHERE ID = %s"""
            cursor.execute(query, [r_id])
            connection.commit()

    def update_restaurant_by_id(self, form, restaurantId, current_user_id):
        self.primaryId = restaurantId
        self.name =  form['Name']
        self.address = form['Address']
        self.contactName = form['contactName']
        self.creatorId =  current_user_id
        self.score = 0
        self.profilePicture = form['Photo']
        self.hours = form['WorkingHours']
        self.currentStatus = form['CurrentStatus']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE RESTAURANTS SET NAME = %s, ADDRESS = %s, CONTACT_NAME = %s, PROFILE_PICTURE = %s, HOURS = %s, CURRENT_STATUS = %s WHERE ID = %s"""
            cursor.execute(query, [self.name, self.address, self.contactName, self.profilePicture, self.hours, self.currentStatus, self.primaryId])
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

    def check_user_gave_a_star_or_not(self, user_id, restaurant_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM STAR_RESTAURANTS WHERE USER_ID = %s"""
            cursor.execute(query,[user_id])
            users = cursor.fetchall()
        if(users == []):
            return True
        return False

    def give_star_by_id(self, user_id, restaurant_id , score):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM STAR_RESTAURANTS WHERE USER_ID = %s"""
            cursor.execute(query,[user_id])
            users = cursor.fetchall()
        if (users == []):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO STAR_RESTAURANTS (USER_ID, RESTAURANT_ID, STAR)
                    VALUES (%s,%s,%s)"""
                cursor.execute(query, [int(user_id), int(restaurant_id), int(score)])
                connection.commit()
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """SELECT * FROM STAR_RESTAURANTS WHERE RESTAURANT_ID = %s"""
                cursor.execute(query,[restaurant_id])
                stars = cursor.fetchall()

            totalStar = 0;
            count = 0;
            for i in stars:
                totalStar += i[3]
                count += 1
            updatedScore = totalStar/count


            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """UPDATE RESTAURANTS SET SCORE = %s WHERE ID = %s"""
                cursor.execute(query, [updatedScore, restaurant_id])
                connection.commit()

    def take_food_to_restaurant(self, foods, drinks, restaurant_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM RESTAURANT_FOODS"""
            cursor.execute(query, [restaurant_id])
            current_foods = cursor.fetchall()
        foods_new = []
        for i in foods:
            for j in current_foods:
                if(str(j[1]) == str(restaurant_id) and str(j[2]) == str(i)):
                    foods_new.append(i)
        foods = list(set(foods) - set(foods_new))
        for i in foods:
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO RESTAURANT_FOODS (FOOD_ID, RESTAURANT_ID, SELL_COUNT)
                    VALUES (%s,%s,%s)"""
                cursor.execute(query, [i, restaurant_id, 0])
                connection.commit()
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM RESTAURANT_DRINKS"""
            cursor.execute(query, [restaurant_id])
            current_drinks = cursor.fetchall()
        drinks_new = []
        for i in drinks:
            for j in current_drinks:
                if(str(j[1]) == str(restaurant_id) and str(j[2]) == str(i)):
                    drinks_new.append(i)
        drinks = list(set(drinks) - set(drinks_new))
        for i in drinks:
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO RESTAURANT_DRINKS (DRINK_ID, RESTAURANT_ID, SELL_COUNT)
                    VALUES (%s,%s,%s)"""
                cursor.execute(query, [int(i), int(restaurant_id), 0])
                connection.commit()

    def get_food_and_drink(self,restaurant_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM RESTAURANT_FOODS JOIN FOODS ON RESTAURANT_FOODS.FOOD_ID = FOODS.ID WHERE RESTAURANT_ID = %s"""
            cursor.execute(query, [restaurant_id])
            foods = cursor.fetchall()
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM RESTAURANT_DRINKS JOIN DRINKS ON RESTAURANT_DRINKS.DRINK_ID = DRINKS.ID WHERE RESTAURANT_ID = %s"""
            cursor.execute(query, [restaurant_id])
            drinks = cursor.fetchall()
        return (foods,drinks)


def delete_food_from_restaurant(restaurant_id,food_id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            DELETE FROM RESTAURANT_FOODS WHERE RESTAURANT_ID = %s AND FOOD_ID = %s"""
        cursor.execute(query, [restaurant_id,food_id] )
        connection.commit()
def delete_drink_from_restaurant(restaurant_id,drink_id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            DELETE FROM RESTAURANT_DRINKS WHERE RESTAURANT_ID = %s AND DRINK_ID = %s"""
        cursor.execute(query, [restaurant_id,drink_id] )
        connection.commit()
def find_restaurant_id_by_name(restaurant_name):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT ID FROM RESTAURANTS WHERE NAME = %s"""
        cursor.execute(query, [r_id])
        value = cursor.fetchone()
        empty = {}
        if value is not None:
            return value
        else:
            return None
