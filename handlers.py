from flask import Blueprint, render_template , redirect , current_app,url_for
from flask import request,flash,session
from datetime import datetime
from flask_login import LoginManager,login_user,login_required,current_user
from flask_login import logout_user
from passlib.apps import custom_app_context as pwd_context
import psycopg2 as dbapi2

from classes.messages import *
from classes.drinks import *
from classes.events import *
from classes.event_control_functions import *
from classes.drink_control_functions import *
import classes.achievements as achievementMod
from classes.deals import Deals
site = Blueprint('site', __name__)


from classes.users import *
from server import load_user

def abort(code):
    if code == 401:
        return "You don't have authorize to access this page!"

@site.route('/logout')
def logout_page():
    logout_user()
    session['logged_in'] = False
    session['name'] = ''
    session['id'] = 0
    return redirect(url_for('site.home_page',firstEvent=None,eventDic=None))

@site.route('/', methods=['GET', 'POST'])
def home_page():
    events = select_all_events()
    eventList = []
    firstEvent = None
    for eventNum,eventSelect in enumerate(events):
        if eventNum == 0:#Create event objects
            firstEvent = Events(select = eventSelect)
        else:
            eventList.append(Events(select = eventSelect))
    #return render_template('home/index.html',firstEvent = firstEvent,eventDic = eventList)
    if request.method == 'GET':
        return render_template('home/index.html',firstEvent = None,eventDic = None)
    else:
        input_mail = request.form['InputEmail']
        input_password = request.form['InputPassword']
        if input_mail in current_app.config['ADMIN_USERS'] and pwd_context.verify(input_password,current_app.config['PASSWORD'][0]) is True:
            user= load_user(input_mail)
            login_user(user)
            session['logged_in'] = True
            session['name'] = user.get_name() + ' ' + user.get_lastname()
            session['id'] = user.get_Id()
            flash( current_user.get_mail())

            return render_template('home/index.html',firstEvent = firstEvent,eventDic = eventList)
          
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT MAIL FROM USERS WHERE MAIL = %s"""
            cursor.execute(statement, [input_mail])
            db_mail = cursor.fetchone()
            if db_mail is not None:  # check whether the user exists
                user = load_user(db_mail)
                statement = """SELECT PASSWORD FROM USERS WHERE MAIL = %s"""
                cursor.execute(statement,[db_mail])
                if pwd_context.verify(input_password,user.Password) is True:
                    login_user(user)
                    session['logged_in'] = True
                    session['name'] = user.get_name() + ' ' + user.get_lastname()
                    session['id'] = user.get_Id()
                    flash( current_user.get_mail())

                    return render_template('home/index.html',firstEvent = firstEvent,eventDic = eventList)
                else:
                    return render_template('home/index.html',firstEvent = firstEvent,eventDic = eventList) #Couldn't login
            else:
                return render_template('home/index.html',firstEvent = firstEvent,eventDic = eventList)






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
@login_required
def initialize_database():
    user = load_user(current_user.get_id())
    if not user.is_admin :
        abort(401)

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
           FOOD_ID INTEGER  NOT NULL,
           SELL_COUNT INTEGER NOT NULL
        );"""
        cursor.execute(query)

        query = """CREATE TABLE ACHIEVEMENTS (
           ID SERIAL PRIMARY KEY,
           NAME VARCHAR(80) NOT NULL,
           ICON VARCHAR(255) NOT NULL,
           CONTENT VARCHAR(80) NOT NULL,
           GOAL INTEGER NOT NULL,
           ENDDATE DATE NOT NULL
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
           ADDRESS VARCHAR(255) NOT NULL,
           CONTACT_NAME VARCHAR(80) NOT NULL,
           CONTACT_PHONE VARCHAR(80) NOT NULL,
           SCORE INTEGER NOT NULL DEFAULT 0 CHECK( SCORE >= 0 AND SCORE <= 5),
           PROFILE_PICTURE VARCHAR(150) NOT NULL,
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
        BIO VARCHAR(500) NOT NULL,
        CITY VARCHAR(80) NOT NULL,
        GENDER VARCHAR(20),
        USERTYPE INTEGER NOT NULL,
        AVATAR VARCHAR(255)
        );"""
        cursor.execute(query)

        query = """CREATE TABLE MESSAGES (
        ID SERIAL PRIMARY KEY,
        SENDER INTEGER REFERENCES USERS(ID) NOT NULL,
        RECEIVER INTEGER REFERENCES USERS(ID) NOT NULL,
        TOPIC VARCHAR(80) NOT NULL,
        CONTENT VARCHAR(800) NOT NULL,
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

        query = """
               INSERT INTO USERS (FIRSTNAME, LASTNAME, MAIL, PASSWORD, BIRTHDATE, CITY,GENDER,USERTYPE,AVATAR)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        hashed_password = pwd_context.encrypt("12345")
        cursor.execute(query, ("admin", "admin", "admin@restoranlandin.com", hashed_password, "10.10.2012", "","",0,"avatar"))
        connection.commit()




        return redirect(url_for('site.home_page'))

@site.route('/restaurants')
def restaurant_home_page():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM RESTAURANTS"""
        cursor.execute(query)
        allValues = cursor.fetchall()
    return render_template('restaurant/index.html', allValues = allValues)

@site.route('/restaurant/create', methods=['GET','POST'])
def restaurant_create_page():
    if request.method == 'GET':
        return render_template('restaurant/new.html')
    else:
        nameInput = request.form['Name']
        addressInput = request.form['Address']
        contactNameInput = request.form['ContanctName']
        contactPhoneInput = request.form['ContanctPhone']
        photoInput = request.form['Photo']
        workingHoursInput = request.form['WorkingHours']
        currentStatusInput = request.form['CurrentStatus']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO RESTAURANTS (NAME, ADDRESS, CONTACT_NAME, CONTACT_PHONE, PROFILE_PICTURE,HOURS,CURRENT_STATUS)
                VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, [nameInput, addressInput, contactNameInput, contactPhoneInput, photoInput, workingHoursInput, currentStatusInput ])
            connection.commit()
        return redirect(url_for('site.restaurant_home_page'))

@site.route('/restaurant/<int:restaurant_id>/')
@login_required
def restaurant_show_page(restaurant_id):

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM RESTAURANTS WHERE id = %s"""
        cursor.execute(query, [restaurant_id])
        value = cursor.fetchall()
        sendedValue = value[0]
    return render_template('restaurant/show.html', sendedValue = sendedValue)


@site.route('/restaurant/<int:restaurant_id>/delete')
@login_required
def restaurant_delete_func(restaurant_id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """DELETE FROM RESTAURANTS WHERE ID = %s"""
        cursor.execute(query, [restaurant_id])
        connection.commit()
    return redirect(url_for('site.restaurant_home_page'))

@site.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def restaurant_edit_page(restaurant_id):
    if request.method == 'GET':
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM RESTAURANTS WHERE id = %s"""
            cursor.execute(query, [restaurant_id])
            value = cursor.fetchall()
            name = value[0][1]
            address = value[0][2]
            contactName = value[0][3]
            contactPhone = value[0][4]
            score = value[0][5]
            pp = value[0][6]
            hours = value[0][7]
            currentStatus = value[0][8]
    else:
        nameInput = request.form['Name']
        addressInput = request.form['Address']
        contactNameInput = request.form['ContanctName']
        contactPhoneInput = request.form['ContanctPhone']
        photoInput = request.form['Photo']
        workingHoursInput = request.form['WorkingHours']
        currentStatusInput = request.form['CurrentStatus']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE RESTAURANTS SET NAME = %s, ADDRESS = %s, CONTACT_NAME = %s, CONTACT_PHONE = %s, PROFILE_PICTURE = %s, HOURS = %s, CURRENT_STATUS = %s WHERE ID = %s"""
            cursor.execute(query, [nameInput, addressInput, contactNameInput, contactPhoneInput, photoInput, workingHoursInput, currentStatusInput, restaurant_id])
            connection.commit()
        return redirect(url_for('site.restaurant_show_page', restaurant_id = restaurant_id))

    form = request.form
    return render_template('restaurant/edit.html', form = form , address = address, name = name, contactName = contactName, contactPhone = contactPhone, pp = pp, hours = hours, currentStatus = currentStatus)


@site.route('/foods')
def food_home_page():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM FOODS"""
        cursor.execute(query)
        allValues = cursor.fetchall()
        #Fetch all drinks from database
        drinks = select_all_drinks()
        drinkList = []
        for drink in drinks:
            drinkList.append(Drinks(select = drink))

    return render_template('food/index.html', allValues = allValues,drinks = drinkList)

@site.route('/food/create', methods=['GET','POST'])
def food_create_page():
    if request.method == 'GET':
        return render_template('food/new.html')
    else:
        nameInput = request.form['name']
        iconInput = request.form['icon']
        typeNameInput = request.form['type']
        priceInput = request.form['price']
        calorieInput = request.form['calorie']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO FOODS (NAME, ICON, FOOD_TYPE, PRICE, CALORIE)
                VALUES (%s,%s,%s,%s,%s)"""
            cursor.execute(query, [nameInput, iconInput, typeNameInput, priceInput, calorieInput])
            connection.commit()
        return redirect(url_for('site.food_home_page'))

@site.route('/food/<int:food_id>/delete')
def food_delete_func(food_id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """DELETE FROM FOODS WHERE ID = %s"""
        cursor.execute(query, [food_id])
        connection.commit()
    return redirect(url_for('site.food_home_page'))

@site.route('/food/<int:food_id>/edit', methods=['GET','POST'])
def food_edit_page(food_id):
    if request.method == 'GET':
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM FOODS WHERE id = %s"""
            cursor.execute(query, [food_id])
            value = cursor.fetchall()
            name = value[0][1]
            icon = value[0][2]
            food_type = value[0][3]
            price = value[0][4]
            calorie = value[0][5]
    else:
        nameInput = request.form['name']
        iconInput = request.form['icon']
        typeNameInput = request.form['type']
        priceInput = request.form['price']
        calorieInput = request.form['calorie']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE FOODS SET NAME = %s, ICON = %s, FOOD_TYPE = %s, PRICE = %s, CALORIE = %s WHERE ID = %s"""
            cursor.execute(query, [nameInput, iconInput, typeNameInput, priceInput, calorieInput, food_id])
            connection.commit()
        return redirect(url_for('site.food_home_page'))

    form = request.form
    return render_template('food/edit.html', form = form, name = name, icon = icon, food_type = food_type, price = price, calorie = calorie)

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
            bio = request.form['bio']
            city = request.form['city']
            gender = request.form['gender']
            userType = request.form['userType']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """
                    INSERT INTO USERS (FIRSTNAME, LASTNAME, MAIL, PASSWORD, BIRTHDATE, BIO, CITY, GENDER, USERTYPE, AVATAR)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                cursor.execute(query, (firstName, lastName, email, hashed_password, birthDate, bio, city, gender, userType, "avatar"))
                connection.commit()
            return redirect(url_for('site.home_page'))

        form = request.form
        return render_template('register/index.html',form=form)


@site.route('/user/<int:user_id>/messages')
@login_required
def messages_home_page(user_id):
    all_messages = select_all_messages(user_id)
    return render_template('messages/index.html',messages = all_messages)

@site.route('/user/<int:user_id>/messages/new',methods=['GET','POST'])
@login_required
def messages_new_page(user_id):
    if request.method == 'GET':
        return render_template('messages/new.html',form=None)
    else:
        receiver = request.form['message_target']
        sender = session['id']
        topic = request.form['message_topic']
        body = request.form['message_body']
        time = datetime.now()
        form = request.form
        valid = validate_message_data(form)
        if valid:
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT ID FROM USERS WHERE MAIL = %s"""
                cursor.execute(statement,[receiver])
                receiver_id = cursor.fetchone()

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """
                    INSERT INTO MESSAGES (SENDER,RECEIVER,TOPIC,CONTENT,SENDDATE)
                    VALUES (%s,%s,%s,%s,%s)"""

                cursor.execute(query, (sender,receiver_id,topic,body,time))
                connection.commit()
            return redirect(url_for('site.messages_home_page',user_id=sender))
        else:
            return  render_template('messages/new.html',form=form)


@site.route('/user/15') #Change me with model [ID]
@login_required
def user_show_page():
    return render_template('user/show.html')

@site.route('/user/15/edit') #Change me with model [ID]
@login_required
def user_edit_page():
    if request.method == 'GET':
        return render_template('user/edit.html',form=None)
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
            bio = request.form['bio']
            city = request.form['city']
            gender = request.form['gender']
            userType = request.form['userType']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """
                    UPDATE USERS
                        SET FIRSTNAME = %s,
                            LASTNAME = %s,
                            MAIL = %s,
                            PASSWORD = %s,
                            BIRTHDATE = %s,
                            BIO = %s,
                            CITY = %s,
                            GENDER = %s,
                            USERTYPE = %s,
                            AVATAR = %s WHERE (ID = %s)"""

                cursor.execute(query, (firstName, lastName, email, hashed_password, birthDate, bio, city, gender, userType, "avatar", Id))
                connection.commit()
            return redirect(url_for('site.user_show_page'))

        form = request.form
        return render_template('user/edit.html',form=form)

@site.route('/admin',methods = ['GET','POST'])
@login_required
def admin_page():
    user = load_user(current_user.get_id())
    if not user.is_admin :
        abort(401)
    if request.method == 'POST':
        eventIds = request.form.getlist('eventIDs')
        #delete events which have ids in eventIds list
        for Id in eventIds:
            delete_event_by_id(Id)

        achievement_ids = request.form.getlist('achievement_ids')

        for ach_id in achievement_ids:
            achievementMod.achievement_delete_by_Id(ach_id)


    achievements = achievementMod.achievement_select_all()
    achievementList = []

    for achievement in achievements:
        achievementList.append(achievementMod.Achievements(select = achievement))

    #Fetch all events to list.
    events = select_all_events()
    eventDic = {}
    for event in events:
        eventDic[event[0]] = event[5]

    return render_template('admin/index.html', achievements = achievementList, eventDic = eventDic)


@site.route('/achievement/<int:achievement_id>', methods=['GET','POST'])
def achievement_show_page(achievement_id):
    if request.method == 'GET':
        select = achievementMod.achievement_select_by_Id(achievement_id)
        achievement = achievementMod.Achievements(select=select)
        return render_template('achievement/show.html',achievement = achievement, form=None)
    else:
        achievementMod.achievement_update(request.form, achievement_id)
        return redirect(url_for('site.admin_page'))
        #select = cursor.fetchone()
        #achievement = Achievements(select=select)


@site.route('/achievement/new',methods = ['GET','POST'])
@login_required
def achievement_create_page():
    if request.method == 'GET':
        return render_template('achievement/new.html', form = None)
    else:
        isValid = validate_achievement_data(request.form)
    if isValid:
        #create an object from form and add it to database.
        achievement = achievementMod.Achievements(form = request.form)
        return redirect(url_for('site.admin_page'))
    form = request.form
    return render_template('achievement/new.html',form=form)


@site.route('/event/new',methods = ['GET','POST'])
@login_required
def event_create_page():
    print('ss')
    if request.method == 'GET':
        return render_template('event/new.html',form = None)
    else:
        isValid = validate_event_data(request.form)
        if isValid:
            #create an object from form and add it to database.
            event = Events(form = request.form)
            print('ss')
            return redirect(url_for('site.home_page'))
        form = request.form
        return render_template('event/new.html',form=form)

@site.route('/event/edit/<int:eventId>',methods = ['GET','POST'])
def event_edit_page(eventId):
    #select one element from id
    event = Events(select = select_event_by_id(eventId))
    if request.method == 'GET':
        return render_template('event/edit.html',event = event,form = None)
    else:
        form = request.form
        isValid = validate_event_data(form)
        if isValid:
            #Update this object
            update_event_by_id(form,eventId)
            #After update take it from database again
            event = Events(select = select_event_by_id(eventId))
            return render_template('event/show.html',event = event)
        else:
            return render_template('event/edit.html',event = event,form = form)



@site.route('/event/<int:eventId>')
@login_required
def event_show_page(eventId):
    #select specific event from databse
    select = select_event_by_id(eventId)
    event = Events(select = select)
    return render_template('event/show.html',event = event)

@site.route('/drink/create',methods = ['GET','POST'])
def drink_create_page():
    if request.method == 'GET':
        return render_template('drinks/new.html',form = None)
    else:
        valid = validate_drink_data(request.form)
        if valid:
            drink = Drinks(request.form)
            return render_template('drinks/new.html',form = None)
        form = request.form
        return render_template('drinks/new.html',form=form)

@site.route('/drink/edit/<int:drinkId>',methods = ['GET','POST'])
def drink_edit_page(drinkId):
    #select one element from id
    drink = Drinks(select = select_drink_by_id(drinkId))
    if request.method == 'GET':
        return render_template('drinks/edit.html',drink = drink,form = None)
    else:
        form = request.form
        isValid = validate_drink_data(form)
        if isValid:
            #Update this object
            update_drink_by_id(form,drinkId)
            #After update take it from database again
            drink = Drinks(select = select_drink_by_id(drinkId))
            return redirect(url_for('site.food_home_page'))
        else:
            return render_template('drink/drink.html',drink = drink,form = form)

@site.route('/drink/delete/<int:drinkId>')
def drink_delete_function(drinkId):
    delete_drink_by_id(drinkId)
    return redirect(url_for('site.food_home_page'))

@site.route('/deals/new', methods = ['GET','POST'])
def deals_add_function():
    if request.method == 'GET':
        return render_template('deals/new.html', form=None)
    else:
        form = request.form
        isValid = validate_deal_data(form)

        if isValid:
            deal = Deals(form = form, foodId = 1, restaurantId = 1)
            return render_template('deals/new.html', form=None)



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


def validate_event_data(form):
    if form == None:
        return True
    form.data = {}
    form.error = {}

    if len(form['Name'].strip()) == 0:
        form.error['Name'] = 'Name of the event can not be blank'
    else:
        form.data['Name'] = form['Name']

    if len(form['Explanations'].strip()) == 0:
        form.error['Explanations'] = 'Explanations of the event can not be blank'
    else:
        form.data['Explanations'] = form['Explanations']

    if len(form['place'].strip()) == 0:
        form.error['place'] = 'Place of the event can not be blank'
    else:
        form.data['place'] = form['place']

    if len(form['startDate'].strip()) == 0:
        form.error['startDate'] = 'Starting date of the event can not be blank'
    else:
        form.data['startDate'] = form['startDate']

    if len(form['endDate'].strip()) == 0:
        form.error['endDate'] = 'Ending date of the event can not be blank'
    else:
        form.data['endDate'] = form['endDate']

    return len(form.error) == 0

def validate_drink_data(form):
    if form == None:
        return True
    form.data = {}
    form.error = {}
    print(len(form['Name'].strip()))
    if len(form['Name'].strip()) == 0:
        form.error['Name'] = 'Name of the drink can not be blank'
    else:
        form.data['Name'] = form['Name']

    if len(form['calorie'].strip()) == 0:
        form.error['calorie'] = 'Calorie value must be specified'
    else:
        form.data['calorie'] = form['calorie']

    return len(form.error) == 0


def validate_achievement_data(form):
    if form == None:
        return True
    form.data = {}
    form.error = {}

    if len(form['Name'].strip()) == 0:
        form.error['Name'] = 'Name of the achievement can not be blank'
    else:
        form.data['Name'] = form['Name']

    if len(form['Explanation'].strip()) == 0:
        form.error['Explanation'] = 'Explanation of the achievement can not be blank'
    else:
        form.data['Explanation'] = form['Explanation']

    if len(form['Goal'].strip()) == 0:
        form.error['Goal'] = 'Goal of the achievement can not be blank'
    else:
        form.data['Explanation'] = form['Explanation']

    if len(form['endDate'].strip()) == 0:
        form.error['endDate'] = 'endDate of the achievement can not be blank'
    else:
        form.data['endDate'] = form['endDate']


    return len(form.error) == 0

def validate_deal_data(form):
    if form == None:
        return True
    form.data = {}
    form.error = {}

    if len(form['rate'].strip()) == 0:
        form.error['rate'] = 'Discount rate of the deal can not be blank'
    else:
        form.data['rate'] = form['rate']

    if len(form['ValidDate'].strip()) == 0:
        form.error['ValidDate'] = 'Valid date of the deal can not be blank'
    else:
        form.data['ValidDate'] = form['ValidDate']

    return len(form.error) == 0
