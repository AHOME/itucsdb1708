from flask import Blueprint, render_template , redirect , current_app,url_for
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

        query = """DROP TABLE IF EXISTS "USER";"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS MESSAGE;"""
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

        # Next three queries will be removed after we update our queries
        query = """DROP TABLE IF EXISTS COUNTER;"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER);"""
        cursor.execute(query)
        query = """INSERT INTO COUNTER (N) VALUES(0);"""
        cursor.execute(query)

        #---------------------------------------------------------------------------

        query = """CREATE TABLE EVENT_RESTAURANTS (
           ID INTEGER PRIMARY KEY AUTOINCREMENT,
           EVENT_ID INTEGER  NOT NULL,
           RESTAURANT_ID INTEGER  NOT NULL,
        )"""
        cursor.execute(query)

        query = """CREATE TABLE COMMENTS (
           ID INTEGER PRIMARY KEY AUTOINCREMENT,
           USER_ID INTEGER  NOT NULL,
           RESTAURANT_ID INTEGER  NOT NULL,
           CONTENT VARCHAR(255) NOT NULL,
           SENDDATE TIMESTAMP NOT NULL,
        )"""
        cursor.execute(query)

        query = """CREATE TABLE RESTAURANT_FOODS (
           ID INTEGER PRIMARY KEY AUTOINCREMENT,
           RESTAURANT_ID INTEGER  NOT NULL,
           FOOD_ID INTEGER  NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE ACHIEVEMENTS (
           ID INTEGER PRIMARY KEY AUTOINCREMENT,
           NAME VARCHAR(80) NOT NULL,
           ICON VARCHAR(255) NOT NULL,
           CONTENT VARCHAR(80) NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE FOODS (
           ID INTEGER PRIMARY KEY AUTOINCREMENT,
           NAME VARCHAR(80) NOT NULL,
           ICON VARCHAR(255) NOT NULL,
           FOOD_TYPE VARCHAR(80) NOT NULL,
           PRICE VARCHAR(80) NOT NULL,
           CALORIE VARCHAR(80) NOT NULL
        )"""
        cursor.execute(query)


        query = """CREATE TABLE RESTAURANTS (
           ID INTEGER PRIMARY KEY AUTOINCREMENT,
           NAME VARCHAR(80) NOT NULL,
           ADDRESS INTEGER NOT NULL,
           CONTACT_NAME VARCHAR(80) NOT NULL,
           CONTACT_PHONE VARCHAR(80) NOT NULL,
           SCORE INTEGER NOT NULL DEFAULT 0 CHECK(CONSTRAINT SCORE >= 0 AND SCORE <= 5),
           PROFILE_PICTURE VARCHAR(80) NOT NULL,
           HOURS VARCHAR(80) NOT NULL,
           CURRENT_STATUS VARCHAR(80) NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE "USER" (
        ID INTEGER PRIMARY KEY NOT NULL,
        FIRSTNAME VARCHAR(80) NOT NULL,
        LASTNAME VARCHAR(80) NOT NULL,
        MAIL VARCHAR(80) NOT NULL,
        PASSWORD VARCHAR(80) NOT NULL,
        BIRTHDATE DATE NOT NULL,
        CITY VARCHAR(80) NOT NULL,
        GENDER VARCHAR(20),
        USERTYPE VARCHAR(80) NOT NULL,
        AVATAR VARCHAR(255) );"""
        cursor.execute(query)

        query = """CREATE TABLE MESSAGE (
        ID INTEGER PRIMARY KEY NOT NULL,
        SENDER INTEGER NOT NULL,
        RECEIVER INTEGER NOT NULL,
        TOPIC VARCHAR(80) NOT NULL,
        CONTENT VARCHAR(80) NOT NULL,
        SENDDATE TIMESTAMP NOT NULL);"""
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

@site.route('/register')
def register_home_page():
    return render_template('register/index.html')

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
