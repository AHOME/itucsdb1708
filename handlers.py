from flask import Blueprint, render_template , redirect , current_app,url_for
from flask import request
from flask_login import LoginManager
from passlib.apps import custom_app_context as pwd_context

import psycopg2 as dbapi2


site = Blueprint('site', __name__)


@site.route('/')
def home_page():
    return render_template('home/index.html')

@site.route('/count') #This page meant for test the database, will be deleted after stability updates
def counter_page():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times." % count


@site.route('/initdb')
def initialize_database():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS USERS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS MESSAGES;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS FOODS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS RESTAURANTS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS ACHIEVEMENTS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS RESTAURANT_FOODS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS COMMENTS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS EVENT_RESTAURANTS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS DRINKS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS EVENTS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS DEALS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS ORDERS;"""
        cursor.execute(query)

        # Next three queries will be removed after we update our queries
        query = """DROP TABLE IF EXISTS COUNTER;"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER);"""
        cursor.execute(query)
        query = """INSERT INTO COUNTER (N) VALUES(0);"""
        cursor.execute(query)

        #---------------------------------------------------------------------------

        query = """CREATE TABLE EVENT_RESTAURANTS (
           ID SERIAL PRIMARY KEY,
           EVENT_ID INTEGER  NOT NULL,
           RESTAURANT_ID INTEGER  NOT NULL
        );"""
        cursor.execute(query)

        query = """CREATE TABLE COMMENTS (
           ID SERIAL PRIMARY KEY,
           USER_ID INTEGER  NOT NULL,
           RESTAURANT_ID INTEGER  NOT NULL,
           CONTENT VARCHAR(255) NOT NULL,
           SENDDATE TIMESTAMP NOT NULL
        );"""
        cursor.execute(query)

        query = """CREATE TABLE RESTAURANT_FOODS (
           ID SERIAL PRIMARY KEY,
           RESTAURANT_ID INTEGER  NOT NULL,
           FOOD_ID INTEGER  NOT NULL
        );"""
        cursor.execute(query)

        query = """CREATE TABLE ACHIEVEMENTS (
           ID SERIAL PRIMARY KEY,
           NAME VARCHAR(80) NOT NULL,
           ICON VARCHAR(255) NOT NULL,
           CONTENT VARCHAR(80) NOT NULL
        );"""
        cursor.execute(query)

        query = """CREATE TABLE FOODS (
           ID SERIAL PRIMARY KEY,
           NAME VARCHAR(80) NOT NULL,
           ICON VARCHAR(255) NOT NULL,
           FOOD_TYPE VARCHAR(80) NOT NULL,
           PRICE VARCHAR(80) NOT NULL,
           CALORIE VARCHAR(80) NOT NULL
        );"""
        cursor.execute(query)

        query = """CREATE TABLE RESTAURANTS (
           ID SERIAL PRIMARY KEY,
           NAME VARCHAR(80) NOT NULL,
           ADDRESS INTEGER NOT NULL,
           CONTACT_NAME VARCHAR(80) NOT NULL,
           CONTACT_PHONE VARCHAR(80) NOT NULL,
           SCORE INTEGER NOT NULL DEFAULT 0 CHECK( SCORE >= 0 AND SCORE <= 5),
           PROFILE_PICTURE VARCHAR(80) NOT NULL,
           HOURS VARCHAR(80) NOT NULL,
           CURRENT_STATUS VARCHAR(80) NOT NULL
        );"""
        cursor.execute(query)

        query = """CREATE TABLE USERS (
        ID SERIAL PRIMARY KEY,
        FIRSTNAME VARCHAR(80) NOT NULL,
        LASTNAME VARCHAR(80) NOT NULL,
        MAIL VARCHAR(80) NOT NULL,
        PASSWORD VARCHAR(500) NOT NULL,
        BIRTHDATE DATE NOT NULL,
        CITY VARCHAR(80) NOT NULL,
        GENDER VARCHAR(20),
        USERTYPE INTEGER NOT NULL,


        AVATAR VARCHAR(255)
        );"""
        cursor.execute(query)

        query = """CREATE TABLE MESSAGES (
        ID SERIAL PRIMARY KEY,
        SENDER INTEGER NOT NULL,
        RECEIVER INTEGER NOT NULL,
        TOPIC VARCHAR(80) NOT NULL,
        CONTENT VARCHAR(80) NOT NULL,
        SENDDATE TIMESTAMP NOT NULL
        );"""
        cursor.execute(query)
        
        query = """CREATE TABLE DRINKS(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(20) NOT NULL,
        TYPE BOOLEAN,
        CALORIE INTEGER,
        DRINKCOLD BOOLEAN,
        ALCOHOL BOOLEAN
        );"""

        cursor.execute(query)

        query = """CREATE TABLE EVENTS(
        ID SERIAL PRIMARY KEY,
        CONTENT VARCHAR(255) NOT NULL,
        ADDRESS VARCHAR(255) NOT NULL,
        STARTINGDATE DATE NOT NULL,
        ENDINGDATE DATE NOT NULL,
        NAME VARCHAR(140) NOT NULL,
        ICON VARCHAR(255)
        );"""

        cursor.execute(query)
        
        query = """CREATE TABLE DEALS (
        ID SERIAL PRIMARY KEY,
        FOOD_ID INTEGER NOT NULL,
        REST_ID INTEGER NOT NULL,
        DATE DATE NOT NULL,
        DISCOUNT_RATE INTEGER NOT NULL CHECK(DISCOUNT_RATE >= 0 AND DISCOUNT_RATE <= 100)
        );"""
        cursor.execute(query)

        query = """CREATE TABLE ORDERS (
        ID SERIAL PRIMARY KEY,
        USER_ID INTEGER NOT NULL,
        REST_ID INTEGER NOT NULL,
        PRICE VARCHAR(80) NOT NULL,
        DATE DATE NOT NULL,
        STATUS VARCHAR(80) NOT NULL
        );"""
        cursor.execute(query)
        
        connection.commit()
        return redirect(url_for('site.home_page'))

@site.route('/restaurant')
def restaurant_home_page():
    return render_template('restaurant/index.html')

@site.route('/restaurant/12') #Change me with model [ID]
def restaurant_show_page():
    return render_template('restaurant/show.html')

@site.route('/restaurant/12/edit')
def restaurant_edit_page():
    return render_template('restaurant/edit.html')

@site.route('/user/12/restaurant/new')
def restaurant_new_page():
    return render_template('restaurant/new.html')

@site.route('/register', methods=['GET','POST'])
def register_home_page():
    if request.method == 'GET':
        return render_template('register/index.html',form=None)
    else:
        valid = validate_user_data(request.form)
        if valid:
            name = request.form['firstName']
            nameList= name.split(" ")
            if(len(nameList) >= 2):
                firstName = nameList[0]
                lastName = nameList[1]
            elif(len(nameList) <2):
                firstName = nameList[0]
                lastName=""
            email = request.form['email']
            password = request.form['password']
            hashed_password = pwd_context.encrypt(password)
            birthDate = request.form['birthDate']
            city = request.form['city']
            gender = request.form['gender']
            userType = request.form['userType']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """
                    INSERT INTO USERS (FIRSTNAME, LASTNAME, MAIL, PASSWORD, BIRTHDATE, CITY,GENDER,USERTYPE,AVATAR) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                cursor.execute(query, (firstName, lastName, email, hashed_password, birthDate, city,gender,userType,"avatar"))
                connection.commit()
            return redirect(url_for('site.home_page'))
        
        form = request.form
        return render_template('register/index.html',form=form)

@site.route('/user/12/message')
def messages_home_page():
    return render_template('messages/index.html')

@site.route('/user/12/message/new') #Change me with model [ID]
def messages_new_page():
    return render_template('messages/new.html')

@site.route('/user/15') #Change me with model [ID]
def user_show_page():
    return render_template('user/show.html')

@site.route('/user/15/edit') #Change me with model [ID]
def user_edit_page():
    return render_template('user/edit.html')

@site.route('/admin')
def admin_page():
    return render_template('admin/index.html')

@site.route('/event/new')
def event_create_page():
    return render_template('event/new.html')

@site.route('/achievement/new')
def achievement_create_page():
    return render_template('achievement/new.html')

@site.route('/event/12')
def event_show_page():
        return render_template('event/show.html')


def validate_user_data(form):
    if form == None: 
        return true

    form.data = {}
    form.errors = {}

    if len(form['firstName'].strip()) == 0:
        form.errors['firstName'] = 'Name can not be blank'
    else:
        form.data['firstName'] = form['firstName']

    if len(form['email'].strip()) == 0:
        form.errors['email'] = 'Email can not be blank'
    else:
        form.data['email'] = form['email']

    if len(form['birthDate'].strip()) == 0:
        form.errors['birthDate'] = 'Birthdate can not be blank'
    else:
        form.data['birthDate'] = form['birthDate']

    if not form['userType']:
        form.errors['userType'] = 'User type can not be blank' 
    else:
        form.data['userType'] = form['userType']

    if form['terms'] == 0:
        form.errors['terms'] = 'You should accept the terms'
    else:
        form.data['terms'] = form['terms']

    return len(form.errors) == 0


