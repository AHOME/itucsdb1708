from flask import Blueprint, render_template , redirect , current_app,url_for
from flask import request,flash,session
from datetime import datetime as dt
from flask_login import LoginManager,login_user,login_required,current_user
from flask_login import logout_user
from passlib.apps import custom_app_context as pwd_context
import psycopg2 as dbapi2

from classes.messages import *
from classes.drinks import *
from classes.news import *
from classes.foods import *
from classes.events import *
from classes.restaurants import *
from classes.food_orders import *
from classes.drink_orders import *
from classes.event_control_functions import *
from classes.drink_control_functions import *
import classes.event_restaurants as EventRestaurantFile
from classes.achievement_user import select_completed_achievements_by_userID
import classes.achievements as achievementMod
from classes.deals import *
site = Blueprint('site', __name__)


from classes.users import *
from server import load_user


@site.route('/logout')
def logout_page():
    logout_user()
    session['logged_in'] = False
    return redirect(url_for('site.home_page',firstEvent=None,eventDic=None,news=None))


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

    newList = get_all_news()


    if request.method == 'GET':
        return render_template('home/index.html',firstEvent = firstEvent,eventDic = eventList,news=newList)
    else:
        input_mail = request.form['InputEmail']
        input_password = request.form['InputPassword']
        if input_mail in current_app.config['ADMIN_USERS'] and pwd_context.verify(input_password,current_app.config['PASSWORD'][0]) is True:
            user= load_user(input_mail)
            login_user(user)
            session['logged_in'] = True
            flash('You have successfully logged in!','user_login')
            return render_template('home/index.html',firstEvent = firstEvent,eventDic = eventList,news=newList)

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
                    flash('You have successfully logged in!','user_login')
                    return render_template('home/index.html',firstEvent = firstEvent,eventDic = eventList,news=newList)
                else:
                    flash('Either mail or password is wrong!','user_login')
                    return render_template('home/index.html',firstEvent = firstEvent,eventDic = eventList,news=newList) #Couldn't login
            else:
                flash('Either mail or password is wrong!','user_login')
                return render_template('home/index.html',firstEvent = firstEvent,eventDic = eventList,news=newList)

@site.route('/results', methods=['GET', 'POST'])
def home_page_search():
    toSearch = request.form['searchbar']
    if toSearch=="" or toSearch==" ":
        return render_template('search/index.html')
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        searchFormatted = '%' + toSearch.lower() + '%'
        query = """SELECT MAIL FROM USERS WHERE LOWER(FIRSTNAME) LIKE %s OR LOWER(LASTNAME) LIKE %s"""
        cursor.execute(query, [searchFormatted,searchFormatted])
        userMailList = cursor.fetchall()

        userList = []
        for mail in userMailList:
            userList.append(get_user(mail))

        query = """SELECT * FROM RESTAURANTS WHERE LOWER(NAME) LIKE %s"""
        cursor.execute(query, [searchFormatted])
        restaurantList = cursor.fetchall()
        restaurants = []

        for rest in restaurantList:
            newRestaurant = Restaurant()
            newRestaurant.create_restaurant_with_attributes(rest[0], rest[1],rest[2],rest[3],rest[4],rest[5],rest[6],rest[7],rest[8])
            restaurants.append(newRestaurant)

    return render_template('search/index.html', users=userList, restaurants=restaurants, searched=toSearch)

@site.route('/initdb')
@login_required
def initialize_database():
    user = load_user(current_user.get_id())
    if not user.is_admin :
        return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The server could not verify that you are authorized to access the URL requested.  You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.</p>"""


    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS ACHIEVEMENT_USER"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS NEWS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS MESSAGES;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS RESTAURANT_FOODS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS STAR_RESTAURANTS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS RESTAURANT_DRINKS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS ACHIEVEMENTS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS COMMENTS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS EVENT_RESTAURANTS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS EVENTS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS DEALS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS FOOD_ORDERS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS DRINK_ORDERS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS DRINKS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS RESTAURANTS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS FOODS;"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS USERS;"""


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
        AVATAR VARCHAR(255),
        BIO VARCHAR(500) NOT NULL
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
           CREATOR_ID INTEGER REFERENCES USERS(ID),
           SCORE INTEGER NOT NULL DEFAULT 0 CHECK( SCORE >= 0 AND SCORE <= 5),
           PROFILE_PICTURE VARCHAR(500) NOT NULL,
           HOURS VARCHAR(80) NOT NULL,
           CURRENT_STATUS VARCHAR(80) NOT NULL
        );"""
        cursor.execute(query)



        query = """CREATE TABLE DRINKS(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(20) NOT NULL,
        TYPE BOOLEAN,
        PRICE INTEGER,
        CALORIE INTEGER,
        DRINKCOLD BOOLEAN,
        ALCOHOL BOOLEAN
        );"""
        cursor.execute(query)

        query = """CREATE TABLE RESTAURANT_FOODS (
           ID SERIAL PRIMARY KEY,
           RESTAURANT_ID INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE,
           FOOD_ID INTEGER REFERENCES FOODS(ID) ON DELETE CASCADE,
           SELL_COUNT INTEGER NOT NULL
        );"""
        cursor.execute(query)

        query = """CREATE TABLE RESTAURANT_DRINKS (
           ID SERIAL PRIMARY KEY,
           RESTAURANT_ID INTEGER  REFERENCES RESTAURANTS(ID) ON DELETE CASCADE,
           DRINK_ID INTEGER  REFERENCES DRINKS(ID) ON DELETE CASCADE,
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

        query = """CREATE TABLE COMMENTS (
           ID SERIAL PRIMARY KEY,
           USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
           RESTAURANT_ID INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE,
           CONTENT VARCHAR(255) NOT NULL,
           SENDDATE TIMESTAMP NOT NULL
        );"""
        cursor.execute(query)

        query = """CREATE TABLE STAR_RESTAURANTS(
            ID SERIAL PRIMARY KEY,
            USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
            RESTAURANT_ID INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE,
            STAR INTEGER NOT NULL
        )
        """
        cursor.execute(query)

        query = """CREATE TABLE MESSAGES (
        ID SERIAL PRIMARY KEY,
        SENDER INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
        RECEIVER INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
        TOPIC VARCHAR(80) NOT NULL,
        CONTENT VARCHAR(800) NOT NULL,
        SENDDATE TIMESTAMP NOT NULL
        );"""
        cursor.execute(query)




        query = """CREATE TABLE EVENTS(
        ID SERIAL PRIMARY KEY,
        CONTENT VARCHAR(255) NOT NULL,
        ADDRESS VARCHAR(255) NOT NULL,
        STARTINGDATE DATE NOT NULL,
        ENDINGDATE DATE NOT NULL,
        NAME VARCHAR(140) NOT NULL,
        ICON VARCHAR(800)
        );"""

        cursor.execute(query)

        query = """CREATE TABLE DEALS (
        ID SERIAL PRIMARY KEY,
        FOOD_ID INTEGER REFERENCES FOODS(ID) ON DELETE CASCADE,
        REST_ID INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE,
        DATE DATE NOT NULL,
        DISCOUNT_RATE INTEGER NOT NULL CHECK(DISCOUNT_RATE >= 0 AND DISCOUNT_RATE <= 100)
        );"""
        cursor.execute(query)

        query = """CREATE TABLE EVENT_RESTAURANTS (
            ID SERIAL PRIMARY KEY,
            EVENT_ID INTEGER REFERENCES EVENTS(ID) ON DELETE CASCADE,
            USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE
            );"""
        cursor.execute(query)

        query = """CREATE TABLE FOOD_ORDERS (
        ID SERIAL PRIMARY KEY,
        USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
        REST_ID INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE,
        FOOD_ID INTEGER REFERENCES FOODS(ID) ON DELETE CASCADE,
        PRICE VARCHAR(80) NOT NULL,
        BUYDATE DATE NOT NULL,
        STATUS VARCHAR(80) NOT NULL
        );"""
        cursor.execute(query)

        query = """CREATE TABLE DRINK_ORDERS (
        ID SERIAL PRIMARY KEY,
        USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
        REST_ID INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE,
        DRINK_ID INTEGER REFERENCES DRINKS(ID) ON DELETE CASCADE,
        PRICE VARCHAR(80) NOT NULL,
        BUYDATE DATE NOT NULL,
        STATUS VARCHAR(80) NOT NULL
        );"""
        cursor.execute(query)


        query = """CREATE TABLE NEWS (
        ID SERIAL PRIMARY KEY,
        TOPIC VARCHAR(80) NOT NULL,
        CONTENT VARCHAR(800) NOT NULL,
        LINK VARCHAR(200),
        RESTAURANT INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE
        );"""

        cursor.execute(query)
        query = """CREATE TABLE ACHIEVEMENT_USER (
        ID SERIAL PRIMARY KEY,
        USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE,
        ACH_ID INTEGER REFERENCES ACHIEVEMENTS(ID) ON DELETE CASCADE,
        USER_ACHIEVED INTEGER NOT NULL
        );"""
        cursor.execute(query)

        connection.commit()

        query = """
               INSERT INTO USERS (FIRSTNAME, LASTNAME, MAIL, PASSWORD, BIRTHDATE, CITY,GENDER,USERTYPE,AVATAR,BIO)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        hashed_password = pwd_context.encrypt("12345")
        cursor.execute(query, ("admin", "admin", "admin@restoranlandin.com", hashed_password, "2012-10-10", "","",0,"avatar",""))
        connection.commit()

        #Add achievements.
        query = """
                INSERT INTO ACHIEVEMENTS (NAME, ICON, CONTENT, GOAL, ENDDATE)
                    VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(query,["First Order","", "Give your first order from any restaurant.", "1", "2020-10-10"])
        connection.commit()


        query = """
                INSERT INTO ACHIEVEMENTS (NAME, ICON, CONTENT, GOAL, ENDDATE)
                    VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(query,["Carnivorous","", "Give 10 orders", "10", "2020-10-10"])
        connection.commit()

        query = """
                INSERT INTO ACHIEVEMENTS (NAME, ICON, CONTENT, GOAL, ENDDATE)
                    VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(query,["Eating Less","", "Give 10 orders that includes meat.", "10", "2020-10-10"])
        connection.commit()

        return redirect(url_for('site.home_page'))

@site.route('/restaurants')
def restaurant_home_page():
    restaurants = Restaurant()
    allValues = restaurants.select_all_restaurants()
    return render_template('restaurant/index.html', allValues = allValues)

@site.route('/restaurant/<int:restaurant_id>/')
def restaurant_show_page(restaurant_id, methods=['GET','POST']):
    restaurant = Restaurant()
    restaurant.select_restaurant_by_id(restaurant_id)

    check = True
    if current_user.is_authenticated :
        check = restaurant.check_user_gave_a_star_or_not(current_user.Id,restaurant_id)
    comments = restaurant.select_all_comments(restaurant_id)
    foods,drinks = restaurant.get_food_and_drink(restaurant_id)

    best_seller_food = [0,""]
    best_seller_drink = [0,""]
    all_foods,all_drinks = restaurant.get_food_and_drink(restaurant_id)
    for i in all_foods:
        if (int(i[3]) > int(best_seller_food[0])):
            best_seller_food[0] = int(i[3])
            best_seller_food[1] = i[5]

    dealList = select_deals_of_restaurant(restaurant_id)
    return render_template('restaurant/show.html', restaurant = restaurant,restaurant_id = restaurant_id, comments = comments, check = check, best_seller_food = best_seller_food[1], foods = all_foods, drinks = all_drinks, deals = dealList)


@site.route('/restaurant/create', methods=['GET','POST'])
def restaurant_create_page():
    if current_user.is_authenticated:
        user_type = current_user.get_type
        if user_type == 1 or current_user.is_admin:
            if request.method == 'GET':
                return render_template('restaurant/new.html')
            else:
                restaurant = Restaurant()
                restaurant.create_restaurant(request.form, current_user.get_Id)
                return redirect(url_for('site.restaurant_home_page'))
    return redirect(url_for('site.home_page'))

@site.route('/restaurant/<int:restaurant_id>/delete')
@login_required
def restaurant_delete_func(restaurant_id):
    if(current_user.is_admin or current_user.get_type == 1):
        restaurant = Restaurant()
        restaurant.delete_restaurant_by_id(restaurant_id)
    return redirect(url_for('site.restaurant_home_page'))

@site.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def restaurant_edit_page(restaurant_id):
    if current_user.is_authenticated:
        user_type = current_user.get_type
        if user_type == 1 or current_user.is_admin:
            restaurant = Restaurant()
            form = request.form
            if request.method == 'GET':
                restaurant.select_restaurant_by_id(restaurant_id)
            else:
                restaurant.update_restaurant_by_id(form, restaurant_id,current_user.get_Id)
                return redirect(url_for('site.restaurant_show_page', restaurant_id = restaurant_id))
            return render_template('restaurant/edit.html', form = form , address = restaurant.address, name = restaurant.name, contactName = restaurant.contactName, creatorId = restaurant.creatorId, pp = restaurant.profilePicture, hours = restaurant.hours, currentStatus = restaurant.currentStatus)
    return redirect(url_for('site.restaurant_home_page'))


@site.route('/submit_comment', methods=['POST'])
def submit_comment():
    if(current_user.is_authenticated):
        restaurant_id = request.form['restaurant_id']
        restaurant = Restaurant()
        restaurant.create_comment(request.form)
        return redirect(url_for('site.restaurant_show_page', restaurant_id = restaurant_id))
    else:
        return redirect(url_for('site.restaurant_home_page'))

@site.route('/comment/<int:comment_id>/<int:restaurant_id>/delete_comment')
def comment_delete_func(comment_id, restaurant_id):
    if(current_user.is_admin):
        restaurant = Restaurant()
        restaurant.delete_comment_by_id(comment_id)
        return redirect(url_for('site.restaurant_show_page', restaurant_id = restaurant_id))
    return redirect(url_for('site.restaurant_home_page'))

@site.route('/give_star/<user_id>/<restaurant_id>/<score>')
def give_star_func(user_id, restaurant_id, score):
    if current_user.is_authenticated:
        restaurant = Restaurant()
        restaurant.give_star_by_id(user_id, restaurant_id, score)
        return redirect(url_for('site.restaurant_show_page', restaurant_id = restaurant_id))
    return redirect(url_for('site.restaurant_home_page'))

@site.route('/save_foods_to_restaurant', methods=['POST'])
def add_food_to_restaurant_page():
    if current_user.is_admin or current_user.get_type == 1:
        foods = request.form.getlist("food",None)
        drinks = request.form.getlist("drink",None)
        restaurant_id = request.form['restaurant_id']
        print("Restoran: ",restaurant_id)
        restaurant = Restaurant()
        restaurant.take_food_to_restaurant(foods,drinks,restaurant_id)
        return redirect(url_for('site.restaurant_show_page', restaurant_id = restaurant_id))
    return redirect(url_for('site.restaurant_home_page'))

@site.route('/menuitems/<restaurant_id>')
def food_home_page(restaurant_id):
    if current_user.is_admin or current_user.get_type == 1:
        food = Foods()
        foods = food.select_all_foods()
        restaurant = Restaurant()
        drinks = select_all_drinks()
        drinkList = []
        for drink in drinks:
            drinkList.append(Drinks(select = drink))

        restaurant = Restaurant()
        restaurant.select_restaurant_by_id(restaurant_id)
        print("FOOOD: " ,restaurant_id)
        return render_template('food/index.html', foods = foods, drinks = drinkList, restaurant = restaurant,restaurant_id=restaurant_id)
    return redirect(url_for('site.home_page'))

@site.route('/food/order/create/<restaurant_id>/<user_id>/<food>/<price>')
def food_order_create_page(restaurant_id, user_id, food, price):
    if(current_user.is_authenticated):
        order = FoodOrders()
        order.create_foodOrders(restaurant_id, user_id, food, price)
    return redirect(url_for('site.home_page'))

@site.route('/food/order/delete/<int:orderId>')
def delete_food_order(orderId):
    delete_food_order_by_id(orderId)
    return redirect(url_for('site.user_show_page',user_id = current_user.get_Id ))

@site.route('/food/order/update/<int:orderId>')
def update_food_order(orderId):
    update_food_order_by_id(orderId,current_user.get_Id)
    return redirect(url_for('site.user_show_page',user_id = current_user.get_Id ))


@site.route('/drink/order/create/<restaurant_id>/<user_id>/<drink>/<price>')
def drink_order_create_page(restaurant_id, user_id, drink, price):
    if(current_user.is_authenticated):
        order = DrinkOrders()
        order.create_drinkOrders(restaurant_id, user_id, drink, price)
    return redirect(url_for('site.home_page'))

@site.route('/drink/order/delete/<int:orderId>')
def delete_drink_order(orderId):
    delete_drink_order_by_id(orderId)
    return redirect(url_for('site.user_show_page',user_id = current_user.get_Id ))

@site.route('/drink/order/update/<int:orderId>')
def update_drink_order(orderId):
    update_drink_order_by_id(orderId)
    return redirect(url_for('site.user_show_page',user_id = current_user.get_Id ))



@site.route('/food/create', methods=['GET','POST'])
def food_create_page():
    if current_user.is_admin or current_user.get_type == 1:
        if request.method == 'GET':
            return render_template('food/new.html')
        else:
            food = Foods()
            food.create_food(request.form)
            return redirect(url_for('site.restaurant_home_page'))
    return redirect(url_for('site.restaurant_home_page'))

@site.route('/food/<int:food_id>/<int:restaurant_id>/delete')
def food_delete_func(food_id,restaurant_id):
    if current_user.is_admin or current_user.get_type == 1:
        print("sd")
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM FOODS WHERE ID = %s"""
            cursor.execute(query, [food_id])
            connection.commit()
    return redirect(url_for('site.food_home_page',restaurant_id = restaurant_id))

@site.route('/food/<int:food_id>/<int:restaurant_id>/edit', methods=['GET','POST'])
def food_edit_page(food_id,restaurant_id):
    if current_user.is_admin or current_user.get_type == 1:
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
            return redirect(url_for('site.food_home_page',restaurant_id = restaurant_id))

        form = request.form
        return render_template('food/edit.html', form = form, name = name, icon = icon, food_type = food_type, price = price, calorie = calorie)
    return redirect(url_for('site.food_home_page',restaurant_id = restaurant_id))




@site.route('/register', methods=['GET','POST'])
def register_home_page():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('site.home_page'))
        return render_template('register/index.html',form=None)
    else:
        form = request.form
        valid = validate_user_data(form)
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
            avatar = request.form['avatar']


            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """
                    INSERT INTO USERS (FIRSTNAME, LASTNAME, MAIL, PASSWORD, BIRTHDATE, CITY, GENDER, USERTYPE, AVATAR, BIO)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                cursor.execute(query, (firstName, lastName, email, hashed_password, birthDate,city, gender, userType, avatar,bio))
                connection.commit()
            flash('This is great! You have successfully registered! Now you can login via navbar.','user_login')
            return redirect(url_for('site.home_page'))
        else:
            form.errors['notComplete'] = 'We couldn\'t registred you as user please fix your answers.'
        form = request.form

        render_template('home/index.html',form=form)


@site.route('/user/<int:user_id>/messages')
@login_required
def messages_home_page(user_id):
    all_messages = select_all_messages(user_id)
    return render_template('messages/index.html',messages = all_messages)

@site.route('/user/<int:user_id>/messages/new',methods=['GET','POST'])
@login_required
def messages_new_page(user_id):
    if request.method == 'GET':
        return render_template('messages/new.html',form=None,errors=None)
    else:
        form = request.form
        receiver = request.form['message_target']
        sender = current_user.get_Id
        topic = request.form['message_topic']
        body = request.form['message_body']
        time = dt.now()
        errors = {}
        errors['userNotFound'] = 'There is no user with this email'

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT ID FROM USERS WHERE MAIL = %s"""
            cursor.execute(statement,[receiver])
            receiver_id = cursor.fetchone()
        if receiver_id == None:
            return  render_template('messages/new.html',form=form,errors = errors)

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO MESSAGES (SENDER,RECEIVER,TOPIC,CONTENT,SENDDATE)
                VALUES (%s,%s,%s,%s,%s)"""

            cursor.execute(query, (sender,receiver_id,topic,body,time))
            connection.commit()
        return redirect(url_for('site.messages_home_page',user_id=sender))




@site.route('/user/<int:user_id>/show')
@login_required
def user_show_page(user_id):
    userType = current_user.get_type
    recent_drink_orders_notR = select_drink_oders_user_notReceived(user_id)
    recent_drink_orders_rec = select_drink_oders_user_Received(user_id)
    recent_food_orders_notR = select_food_oders_user_notReceived(user_id)
    recent_food_orders_rec = select_food_oders_user_Received(user_id)
    voted_res = get_voted_restaurants(user_id)
    completed_achievements = select_completed_achievements_by_userID(user_id)
    if userType==0:
        return redirect(url_for('site.admin_page'))
    elif userType == 1:
        db_user = get_user(current_user.get_mail)
        restaurants_of_owner = get_restaurants(user_id)
        return render_template('user/show.html',user_id = current_user.get_Id, user=db_user ,restaurants_of_owner = restaurants_of_owner)
    else:
        db_user = get_user(current_user.get_mail)
        return render_template('user/show.html',user_id = current_user.get_Id, user=db_user,foodListNR = recent_food_orders_notR,foodListR = recent_food_orders_rec ,drinkListNR = recent_drink_orders_notR,drinkListR = recent_drink_orders_rec,voted_res = voted_res,completed_achievements = completed_achievements )


@site.route('/user/<int:user_id>/edit',methods=['GET','POST']) #Change me with model [ID]
@login_required
def user_edit_page(user_id):
    if request.method == 'GET':
        db_user = get_user(current_user.get_mail)
        return render_template('user/edit.html',user = db_user,form=None)
    else:
        valid = validate_edit_data(request.form)
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
            birthDate = request.form['birthDate']
            bio = request.form['bio']
            city = request.form['city']
            gender = request.form['gender']
            avatar = request.form['avatar']


            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """
                    UPDATE USERS
                        SET FIRSTNAME = %s,
                            LASTNAME = %s,
                            MAIL = %s,
                            BIRTHDATE = %s,
                            CITY = %s,
                            GENDER = %s,
                            AVATAR = %s,
                            BIO = %s
                        WHERE (ID = %s)"""

                cursor.execute(query, (firstName, lastName, email, birthDate, city, gender, avatar, bio, current_user.get_Id))
                connection.commit()

            db_user = get_user(current_user.get_mail)
            return redirect(url_for('site.user_show_page',user_id=current_user.get_Id,user=db_user))

        form = request.form
        return render_template('user/edit.html',form=form)

@site.route('/admin',methods = ['GET','POST'])
@login_required
def admin_page():
    user = load_user(current_user.get_id())
    if not user.is_admin :
        return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The server could not verify that you are authorized to access the URL requested.  You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.</p>"""
    achievements = achievementMod.achievement_select_all()
    achievementList = []

    for achievement in achievements:
        achievementList.append(achievementMod.Achievements(select = achievement))

    #Fetch all events to list.
    events = select_all_events()
    eventDic = {}
    for event in events:
        eventDic[event[0]] = event[5]
    users = get_user_list()
    restaurant = Restaurant()
    restaurants = restaurant.select_all_restaurants()
    #Pop admin. Do not show him
    users.pop(0)
    if request.method == 'POST':
        eventIds = request.form.getlist('eventIDs',None)
        userIds =  request.form.getlist('userIDs',None)
        restaurantIds = request.form.getlist('restaurantIDs',None)
        achievement_ids = request.form.getlist('achievement_ids')
        #delete events which have ids in eventIds list
        rest = Restaurant()
        for Id in eventIds:
            delete_event_by_id(Id)
        for Id in userIds:
            delete_user_by_id(Id)
        #Fetch events again if any of them deleted
        if eventIds:
            events = select_all_events()
            eventDic = {}
            for event in events:
                eventDic[event[0]] = event[5]
        #After deleting users delete them from atendence list.
        if userIds:
            EventRestaurantFile.delete_unnecessary_rows()
            users = get_user_list()
            users.pop(0)
        #If any restaurant deleted fetch them again.

        for Id in restaurantIds:
            rest.delete_restaurant_by_id(Id)

        if restaurantIds:
            restaurant = Restaurant()
            restaurants = restaurant.select_all_restaurants()

        for ach_id in achievement_ids:
            achievementMod.achievement_delete_by_Id(ach_id)

        targetUserMail = request.form.get('userToSend',None)
        #If any achievement deleted fetch all again.
        if achievement_ids:
            achievements = achievementMod.achievement_select_all()
            achievementList = []
            for achievement in achievements:
                achievementList.append(achievementMod.Achievements(select = achievement))

        #delete events which have ids in eventIds list
        if eventIds is not None:
            for Id in eventIds:
                delete_event_by_id(Id)

        achievement_ids = request.form.getlist('achievement_ids',None)

        if achievement_ids is not None:
            for ach_id in achievement_ids:
                achievementMod.achievement_delete_by_Id(ach_id)
        return render_template('admin/index.html', achievements = achievementList, eventDic = eventDic,targetMail = targetUserMail,usersList = users,restaurantsList = restaurants)
    else:
        return render_template('admin/index.html', achievements = achievementList, eventDic = eventDic,usersList = users,restaurantsList = restaurants)

@site.route('/admin/list_users',methods=['GET','POST'])
def users_list_page():
    if request.method == 'GET':
        user_list = get_user_list()
        return render_template('admin/show_users.html',users=user_list)

@site.route('/achievement/<int:achievement_id>', methods=['GET','POST'])
def achievement_show_page(achievement_id):
    if request.method == 'GET':
        select = achievementMod.achievement_select_by_Id(achievement_id)
        achievement = achievementMod.Achievements(select=select)
        return render_template('achievement/show.html',achievement = achievement, form=None)
    else:
        achievementMod.achievement_update(request.form, achievement_id)
        return redirect(url_for('site.admin_page'))



@site.route('/achievement/new',methods = ['GET','POST'])
@login_required
def achievement_create_page():
    if request.method == 'GET':
        return render_template('achievement/new.html', form = None)
    else:
        achievement = achievementMod.Achievements(form = request.form)
        return redirect(url_for('site.admin_page'))


@site.route('/news/new',methods = ['GET','POST'])
@login_required
def news_create_page():
    if request.method == 'POST':
        form = request.form
        title = form['title']
        content = form['content']
        link = form['link']
        restaurant_name = form['restaurant_name']
        if len(link.strip()) == 0:
            link = ""

        if len(restaurant_name.strip()) == 0:
            restaurant_name = ""
        else:
            Id = find_restaurant_id_by_name(restaurant_name)
            if Id == None:
                restaurant_name = ""

        new_news = News(Topic=title,Content=content,Link=link,Restaurant=restaurant_name)
        new_news.insert_news()
        new_news.find_news_id()
    return redirect(url_for('site.admin_page'))

@site.route('/news/<int:news_id>/edit',methods = ['GET','POST'])
@login_required
def news_edit_page(news_id):
    if request.method == 'POST':
        the_old_news = get_news_by_id(news_id)
        form = request.form
        title = form['header']
        the_old_news.Topic =title
        content = form['content']
        the_old_news.Content =content
        link = form['link']
        restaurant_name = form['restaurant_name']
        if len(link.strip()) == 0:
            link = ""

        the_old_news.Link =link
        if len(restaurant_name.strip()) == 0:
            restaurant_name = ""
        else:
            Id = find_restaurant_id_by_name(restaurant_name)
            if Id == None:
                restaurant_name = ""
        the_old_news.Restaurant =restaurant_name
        the_old_news.update_news()
        flash('You have successfully updated the news','user_login')
        return redirect(url_for('site.home_page'))

    else:
        NewsClass = get_news_by_id(news_id)
        form = {}
        form['id'] = NewsClass.Id
        form['title'] = NewsClass.Topic
        form['content'] =  NewsClass.Content
        form['link'] =  NewsClass.Link
        if NewsClass.Restaurant != None:
            restaurant = Restaurant()
            restaurant.select_restaurant_by_id(NewsClass.Restaurant)
            form['restaurant_name'] = restaurant.name
        else:
            form['restaurant_name'] = ""
        return render_template('news/edit.html',form=form)

@site.route('/news/<int:news_id>/delete')
@login_required
def news_delete_page(news_id):
    delete_news(news_id)
    flash('You have successfully delted the news','user_login')
    return redirect(url_for('site.home_page'))


@site.route('/event/new',methods = ['GET','POST'])
@login_required
def event_create_page():

    if request.method == 'GET':
        return render_template('event/new.html',form = None)
    else:
        isValid = validate_event_data(request.form)
        if isValid:
            #create an object from form and add it to database.
            event = Events(form = request.form)

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
def event_show_page(eventId):
    #select specific event from databse
    is_coming = False
    select = select_event_by_id(eventId)
    event = Events(select = select)
    # fetch people attend this event
    comers = EventRestaurantFile.select_comers_all(eventId)
    if current_user.is_authenticated:
        currentUserId = current_user.get_Id
        is_coming = EventRestaurantFile.does_user_come(currentUserId,eventId)
    #Is person coming
    return render_template('event/show.html',event = event,is_coming = is_coming,comers = comers)

@site.route('/event/<int:eventId>/not_going')
def event_user_not_going(eventId):
    currentUserId = current_user.get_Id
    EventRestaurantFile.delete_comers_by_Id(eventId,currentUserId)
    return redirect(url_for('site.event_show_page',eventId = eventId))

@site.route('/event/<int:eventId>/going')
def event_user_going(eventId):
    currentUserId = current_user.get_Id
    EventRestaurantFile.EventRestaurants(eventId,currentUserId)
    return redirect(url_for('site.event_show_page',eventId = eventId))

@site.route('/drink/create',methods = ['GET','POST'])
def drink_create_page():
    if request.method == 'GET':
        return render_template('drinks/new.html',form = None)
    else:
        drink = Drinks(request.form)
        return render_template('drinks/new.html',form = None)


@site.route('/drink/edit/<int:drinkId>/<int:restaurant_id>',methods = ['GET','POST'])
def drink_edit_page(drinkId,restaurant_id):
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
            return redirect(url_for('site.food_home_page',restaurant_id=restaurant_id))
        else:
            return render_template('drink/drink.html',drink = drink,form = form)

@site.route('/drink/delete/<int:drinkId>/<int:restaurant_id>')
def drink_delete_function(drinkId,restaurant_id):
    delete_drink_by_id(drinkId)
    return redirect(url_for('site.food_home_page',restaurant_id=restaurant_id))

@site.route('/deals/new/<int:restaurant_id>/<int:food_id>', methods = ['GET','POST'])
def deals_add_function(restaurant_id, food_id):
    if request.method == 'GET':
        return render_template('deals/new.html', form=None, restaurant_id=restaurant_id, food_id=food_id)
    else:
        form = request.form

        deal = Deals(form = form, foodId = food_id, restaurantId = restaurant_id)
        return render_template('deals/new.html', form=form)

@site.route('/deals/delete/<int:deal_id>/<int:restaurant_id>', methods = ['GET','POST'])
def deals_delete_function(deal_id, restaurant_id):
    delete_deals_by_Id(deal_id)
    return redirect(url_for('site.restaurant_show_page', restaurant_id = restaurant_id))

@site.route('/deals/edit/<int:deal_id>/<int:restaurant_id>', methods = ['GET','POST'])
def deals_update_function(deal_id, restaurant_id):
    deal = Deals(select = select_deal_by_Id(deal_id))
    if request.method == 'GET':
        return render_template('deals/edit.html',deal = deal,form = None)
    else:
        form = request.form
        update_deal_by_Id(request.form, deal_id)
        return redirect(url_for('site.restaurant_show_page', restaurant_id = restaurant_id))

@site.route('/menu/delete/food/<int:restaurant_id>/<int:food_id>')
def menu_food_delete(restaurant_id,food_id):
    delete_food_from_restaurant(restaurant_id,food_id)
    return redirect(url_for('site.restaurant_show_page',restaurant_id  = restaurant_id ))

@site.route('/menu/delete/drink/<int:restaurant_id>/<int:drink_id>')
def menu_drink_delete(restaurant_id,drink_id):
    delete_drink_from_restaurant(restaurant_id,drink_id)
    return redirect(url_for('site.restaurant_show_page',restaurant_id  = restaurant_id ))


def validate_edit_data(form):
    if form == None:
        return False

    form.data = {}
    form.errors = {}


    form.data['firstName'] = form['firstName']


    form.data['email'] = form['email']


    form.data['birthDate'] = form['birthDate']

    if not form['bio']:
        form.data['bio'] = form['bio']
    if len(form['avatar'].strip()) == 0:
        form.data['avatar']='http://gazettereview.com/wp-content/uploads/2016/03/facebook-avatar.jpg'
    else:
        form.data['avatar'] = form['avatar']

    return len(form.errors) == 0


def validate_user_data(form):
    if form == None:
        return False

    form.data = {}
    form.errors = {}

    form.data['firstName'] = form['firstName']

    form.data['email'] = form['email']

    form.data['birthDate'] = form['birthDate']

    if not form['bio']:
        form.data['bio'] = form['bio']

    if len(form['avatar'].strip()) == 0:
        form.data['avatar']='http://gazettereview.com/wp-content/uploads/2016/03/facebook-avatar.jpg'
    else:
        form.data['avatar'] = form['avatar']



    return len(form.errors) == 0


def validate_event_data(form):
    if form == None:
        return False
    form.data = {}
    form.error = {}

    form.data['Name'] = form['Name']

    form.data['Explanations'] = form['Explanations']

    form.data['place'] = form['place']


    form.data['startDate'] = form['startDate']

    if form['endDate'] < form['startDate']:
        form.error['endDate'] = 'Ending date must be earlier date from starting date'
    else:
        form.data['endDate'] = form['endDate']


    form.data['link'] = form['link']

    return len(form.error) == 0
