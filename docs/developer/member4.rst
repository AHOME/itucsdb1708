Parts Implemented by Burak Bekci
================================
CRUD operations of Events and Drinks table. Delete, read and update operations for food and drink orders create operations was implemented by Sadık Ekin Özbay. Control of achievements.

Events Table
============
Events are one of the social parts of RESTORANLANDIN. It helps restaurant owners and user to meet each other.

Attributes of Events Table
^^^^^^^^^^^^^^^^^^^^^^^^^^

* ID SERIAL PRIMARY KEY
    Primary key of events.
* CONTENT VARCHAR(255) NOT NULL
    Detailed information about events.
* ADDRESS VARCHAR(255) NOT NULL
    Address of event.
* STARTINGDATE DATE NOT NULL
    Starting date of event.
* ENDINGDATE DATE NOT NULL
    Ending date of event.
* NAME VARCHAR(140) NOT NULL
    Name of the event.
* ICON VARCHAR(800)
    Picture of the event.


Operations
^^^^^^^^^^
To operate create, select, update and delete operations a class implemented.

Create
^^^^^^
To add new events constructor of Events class used. This constructor takes either a form or a list. Forms are taken by the user in Event Create Page and
lists are things that SELECT operations returns.

.. code-block:: python

      def __init__(self,form = None,select = None):
          if form is None:#select statement will return list object.
              self.Id = select[0]
              self.content = select[1]
              self.address = select[2]
              self.startDate = select[3]
              self.endDate = select[4]
              self.name = select[5]
              self.iconPath = select[6]
          elif select is None:
              self.Id = ""
              self.content = form['Explanations']
              self.address = form['place']
              self.startDate = form['startDate']
              self.endDate = form['endDate']
              self.name = form['Name']
              self.iconPath = form['link']
              with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  query = """
                      INSERT INTO EVENTS (NAME, ENDINGDATE, CONTENT, ADDRESS, STARTINGDATE,ICON)
                      VALUES (%s,%s,%s,%s,%s,%s)"""
                  cursor.execute(query, [self.name, self.endDate, self.content, self.address, self.startDate,self.iconPath])
                  connection.commit()
              with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  statement = """SELECT * FROM EVENTS WHERE (NAME = %s)
                  AND (ENDINGDATE = %s)
                  AND (CONTENT = %s)
                  AND (ADDRESS = %s)
                  AND (STARTINGDATE = %s)
                  AND (ICON = %s)"""
                  cursor.execute(statement,[self.name,self.endDate, self.content, self.address, self.startDate,self.iconPath ])
                  IdofCurrent = cursor.fetchone()[0]
                  self.Id = IdofCurrent

Select
^^^^^^
There are 2 select methods for events. First, one reads all events and lists them in admin panel and homepage.
Other method is written for showing events on its page.

.. code-block:: python

      def select_all_events():
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """SELECT * FROM EVENTS"""
              cursor.execute(statement)
              events = cursor.fetchall()
              return events

      #Return list that database returns
      def select_event_by_id(Id):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """SELECT * FROM EVENTS WHERE (ID = %s)"""
              cursor.execute(statement,[Id])
              return cursor.fetchone()

Update
^^^^^^
An event can be updated from Event Edit form.

.. code-block:: python

      def update_event_by_id(form,eventId):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """
              UPDATE EVENTS SET NAME = %s,
              ENDINGDATE = %s,
              CONTENT = %s,
              ADDRESS = %s,
              STARTINGDATE = %s,
              ICON = %s
              WHERE (ID = %s)"""
              cursor.execute(statement,[form['Name'],form['endDate'],form['Explanations'], form['place'],form['startDate'],form['link'] ,eventId])
              connection.commit()

Delete
^^^^^^
Events can be deleted by admin from admin panel.

.. code-block:: python

      def delete_event_by_id(Id):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """
              DELETE FROM EVENTS WHERE ID = %s"""
              cursor.execute(query, [Id] )
              connection.commit()

Events deleted by their id.

To attend users to events a connection table is used.

Events-Users Table
==================
This is a connection table to keep which user has attended which event. The name of the table is EVENTS_RESTAURANTS however it is operating with users and events.

Attributes of Events_Users Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ID SERIAL PRIMARY KEY
  Primary key.
* EVENT_ID INTEGER REFERENCES EVENTS(ID) ON DELETE CASCADE
  A foreign key refers to Events table. It helps to take details of events.
* USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE
  A foreign key refers to the Users table. It helps to take the name of the user.

Operations
^^^^^^^^^^

Create, select and delete operations is used.

Create
^^^^^^
Similiar to Events table, inserting a row made in the constructor. This method provokes when the user clicks "Going" button on the event page.

.. code-block:: python

      def __init__(self, eventId, userId):
          self.Id = ""
          self.eventId = eventId
          self.userId = userId
          print(self.userId)
          print(self.eventId)
          with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO EVENT_RESTAURANTS (EVENT_ID, USER_ID)
            VALUES (%s,%s)"""
            cursor.execute(query, [self.eventId, self.userId])
            connection.commit
          with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM EVENT_RESTAURANTS WHERE (EVENT_ID = %s)
            AND (USER_ID = %s)"""
          cursor.execute(statement,[self.eventId, self.userId])
          IdofCurrent = cursor.fetchone()[0]
          self.Id = IdofCurrent

Select
^^^^^^
This method reads the name and surname of users by joining EVENTS_RESTAURANTS and USERS table. It is written to show these names on the events page.

.. code-block:: python

      def select_comers_all(eventId):
          #Select name from user table who comes to that event.
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """SELECT USERS.FIRSTNAME, USERS.LASTNAME FROM EVENT_RESTAURANTS,USERS
              WHERE USERS.ID = EVENT_RESTAURANTS.USER_ID
              AND EVENT_RESTAURANTS.EVENT_ID = %s"""
              cursor.execute(statement,[eventId])
              comers = cursor.fetchall()
              return comers

Also, there is another select method that returns a user attend a specific event or not. This is written to change the button on the event page.

.. code-block:: python

      def does_user_come(userId,eventId):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """SELECT * FROM EVENT_RESTAURANTS
              WHERE USER_ID = %s
              AND EVENT_ID = %s """
              cursor.execute(statement,[userId,eventId])
              comers = cursor.fetchall()
          return comers

Delete
^^^^^^
This method is used when a user selects not to come to the event via "Not Going" button on the event page.

.. code-block:: python

      def delete_comers_by_Id(eventId,userId):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """
              DELETE FROM EVENT_RESTAURANTS WHERE EVENT_ID = %s AND
              USER_ID = %s"""
              cursor.execute(query, [eventId,userId])
              connection.commit()

Drinks Table
============
Drinks are one of the main entities in RESTORANLANDIN. There is a pool in the website that contains all the food and drinks which are added by admin or user.

Attributes of Drinks Table
^^^^^^^^^^^^^^^^^^^^^^^^^^
* ID SERIAL PRIMARY KEY
    Primary key for drinks.
* NAME VARCHAR(20) NOT NULL
    Name of the drink.
* TYPE BOOLEAN
    Variable to keep a drink is acidic or not.
* PRICE INTEGER
    Price of drinks.
* CALORIE INTEGER
    The calorie of drinks.
* DRINKCOLD BOOLEAN
    Is it drinking cold or not.
* ALCOHOL BOOLEAN
    Variable to keep a drink is alcohol-free or not.

Operations
^^^^^^^^^^
To operate create, select, update and delete operations a class implemented.

Create
^^^^^^
To add new drinks constructor of Drinks class used. This constructor takes either a form or a list. Forms are taken by the user in Drink Create page and
lists are things that SELECT operations returns.

.. code-block:: python

      class Drinks():
          def __init__(self, form = None,select  = None):
              if select is None:
                  self.Id = ""
                  self.name = form['Name']
                  self.calorie = form['calorie']
                  self.drinkCold =form['drink_cold']
                  self.alcohol = form['alcohol']
                  self.drinkType = form['Soda']
                  self.price = form['price']
                  with dbapi2.connect(current_app.config['dsn']) as connection:
                      cursor = connection.cursor()
                      query = """
                          INSERT INTO DRINKS (NAME, TYPE, CALORIE, DRINKCOLD, ALCOHOL, PRICE)
                          VALUES (%s,%s,%s,%s,%s, %s)"""
                      cursor.execute(query, [self.name, self.drinkType, self.calorie, self.drinkCold, self.alcohol, self.price])
                      connection.commit()
                  with dbapi2.connect(current_app.config['dsn']) as connection:
                      cursor = connection.cursor()
                      statement = """SELECT * FROM DRINKS WHERE (ALCOHOL = %s)
                      AND (NAME = %s)
                      AND (TYPE = %s)
                      AND (CALORIE = %s)
                      AND (DRINKCOLD = %s)"""
                      cursor.execute(statement,[self.alcohol, self.name, self.drinkType, self.calorie, self.drinkCold])
                      IdofCurrent = cursor.fetchone()[0]
                      self.Id = IdofCurrent
              elif form is None:
                  self.Id = select[0]
                  self.name = select[1]
                  self.calorie = select[3]
                  self.drinkCold = select[4]
                  self.alcohol = select[5]
                  self.drinkType = select[2]

Select
^^^^^^
There are 2 select methods for drinks. The first method reads all drinks and lists them on the menu page.
Other select method is used in restaurants page to get details of drinks.

.. code-block:: python

      def select_all_drinks():
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """SELECT * FROM DRINKS"""
              cursor.execute(statement)
              drinks = cursor.fetchall()
              return drinks

      #Return list that database returns
      def select_drink_by_id(Id):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """SELECT * FROM DRINKS WHERE (ID = %s)"""
              cursor.execute(statement,[Id])
              return cursor.fetchone()

Update
^^^^^^
A drink can be updated from Drink Edit form.

.. code-block:: python

      def update_drink_by_id(form,drinkId):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """
              UPDATE DRINKS SET NAME = %s,
              TYPE = %s,
              CALORIE = %s,
              DRINKCOLD = %s,
              ALCOHOL = %s,
              PRICE = %s
              WHERE (ID = %s)"""
              cursor.execute(statement,[form['Name'],form['Soda'],form['calorie'], form['drink_cold'],form['alcohol'],form['price'], drinkId])
              connection.commit()

The update operation is done by their ids. Restaurant owners and admin can update any attribute of drink except their ids.

Delete
^^^^^^
Drinks can be deleted by admin or restaurant owners with links which are located on the menu page.

.. code-block:: python

      def delete_drink_by_id(Id):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """
                  DELETE FROM DRINKS WHERE ID = %s"""
              cursor.execute(query, [Id] )
              connection.commit()

Drinks deleted by their id.


Users in RESTORANLANDIN can order food or drink from any restaurants they like.

To handle order operations, an order table in the database was necessary. Since foods and drinks have different attributes their order tables are also different.
I implemented search, update and delete operation for drink and food order tables. Create operation implemented by Sadık Ekin Özbay.

Food_Orders Table
=================
RESTORANLANDIN gives an opportunity for their customers to order foods. A database table named FOOD_ORDERS created for orders.

Attributes of Food_Orders Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ID SERIAL PRIMARY KEY
    Primary key for food orders.
* USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE
    A foreign key to fetch information about the user who gave the order.
* REST_ID INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE
    A foreign key to fetch restaurant information.
* FOOD_ID INTEGER REFERENCES FOODS(ID) ON DELETE CASCADE
    A foreign key to reaching food information. This key also helps controlling achievements.
* PRICE VARCHAR(80) NOT NULL
    Price of the food.
* BUYDATE DATE NOT NULL
    Date of the order.
* STATUS VARCHAR(80) NOT NULL
    It is either "Received" or "Not Received" among the lifetime of the database. When the order created first this value is set to "Not Received"
    then users set them to "Received" on their profile page.

Operations
^^^^^^^^^^
Methods implemented in order to insert and updating rows to the database, reading from database and deleting rows from the database.


Select
^^^^^^
Two different methods are used for reading operation. One method fetching food orders which their status attribute equal to "Not Received".

.. code-block:: python

      def select_food_oders_user_notReceived(userID):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """SELECT RESTAURANTS.NAME,FOODS.NAME,FOOD_ORDERS.PRICE,BUYDATE,STATUS,RESTAURANTS.ID,FOOD_ORDERS.ID
              FROM FOOD_ORDERS,RESTAURANTS,FOODS WHERE USER_ID = %s AND
              FOOD_ORDERS.REST_ID = RESTAURANTS.ID AND FOODS.ID = FOOD_ORDERS.FOOD_ID AND FOOD_ORDERS.STATUS = %s"""
              cursor.execute(query, [userID,"Not Recieved"])
              return cursor.fetchall()

The second method selects rows with the value of equal to "Received" for their status attribute.

.. code-block:: python

      def select_food_oders_user_Received(userID):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """SELECT RESTAURANTS.NAME,FOODS.NAME,FOOD_ORDERS.PRICE,BUYDATE,STATUS,RESTAURANTS.ID,FOOD_ORDERS.ID
               FROM FOOD_ORDERS,RESTAURANTS,FOODS WHERE USER_ID = %s AND
              FOOD_ORDERS.REST_ID = RESTAURANTS.ID AND FOODS.ID = FOOD_ORDERS.FOOD_ID AND FOOD_ORDERS.STATUS = %s"""
              cursor.execute(query, [userID,"Received"])
              return cursor.fetchall()

To list the food orders on user's page these 2 methods were used.

Update
^^^^^^
Food orders updated from user's profile page. The function given below provokes when the user clicks the "Finish Order" button on the profile page under the list of Unreceived Orders.
As the name implies, it is the user who finishes orders in RESTORANLANDIN. Status column's of orders was set to "Received".

.. code-block:: python

      def update_food_order_by_id(orderId,user_id):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """
              UPDATE FOOD_ORDERS SET
              STATUS = %s
              WHERE (ID = %s)"""
              cursor.execute(statement,["Received",orderId])
              connection.commit()
          #Find food from its table to update achievements.
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """SELECT FOODS.NAME,FOODS.FOOD_TYPE,FOODS.CALORIE FROM FOODS,FOOD_ORDERS WHERE (FOOD_ORDERS.ID = %s)
              AND (FOODS.ID = FOOD_ID) """
              cursor.execute(query, [orderId])
              food_info = cursor.fetchone()
              add_row(user_id,1) #First order achievement.
              if food_info[1] == "Meat": #Eat meat achievement.
                  add_row(user_id,2)
              if int(food_info[2]) < 100:#Eat healthy achievement.
                  add_row(user_id,3)


This function also helps to control achievements. When the user finishes order positively, relevant achievements controlled.
Relevant achievements found by their attributes, simple selection query was used in order to find relevant achievements.


Delete
^^^^^^
Users may cancel their orders before receiving them. The cancellation process is done by the "Cancel Order" button on the profile page next to "Finish Order" button.
This button provokes the given method below.

.. code-block:: python

      def delete_food_order_by_id(orderId):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """
              DELETE FROM FOOD_ORDERS WHERE ID = %s"""
              cursor.execute(query, [orderId] )
              connection.commit()

Another type of orders in RESTORANLANDIN is drink orders. It has very similar methods for food orders since the main purpose of them is same.

Drink_Orders Table
===================
Drinks can be order from restaurants as well as foods in RESTORANLANDIN.
A database table named DRINK_ORDERS created for drink orders and functions implemented to operate on it.

Attributes of Drinks Table
^^^^^^^^^^^^^^^^^^^^^^^^^^

* ID SERIAL PRIMARY KEY
    Primary key for drink orders.
* USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE
    A foreign key to fetch information about the user who gave the order.
* REST_ID INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE
    A foreign key to fetch restaurant information.
* DRINK_ID INTEGER REFERENCES FOODS(ID) ON DELETE CASCADE
    A foreign key to reaching drink information.
* PRICE VARCHAR(80) NOT NULL
    Price of the drink.
* BUYDATE DATE NOT NULL
    Date of the order.
* STATUS VARCHAR(80) NOT NULL
    It is either "Received" or "Not Received" among the lifetime of the database. When the order created, this value is set to "Not Received"
    then users set them to "Received" on their profile page.


Operations
^^^^^^^^^^
Methods implemented in order to insert and updating rows to the database, reading from database and deleting rows from the database.

Select
^^^^^^
Two different methods are used for selecting operation. For these selection queries a join operation on three tables was written.
One method fetching drink orders which their status attribute equal to "Not Received".

.. code-block:: python

      def select_drink_oders_user_notReceived(userID):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """SELECT RESTAURANTS.NAME,DRINKS.NAME,DRINK_ORDERS.PRICE,BUYDATE,STATUS,RESTAURANTS.ID,DRINK_ORDERS.ID
              FROM DRINK_ORDERS,RESTAURANTS,DRINKS WHERE USER_ID = %s AND
              DRINK_ORDERS.REST_ID = RESTAURANTS.ID AND DRINKS.ID = DRINK_ORDERS.DRINK_ID AND DRINK_ORDERS.STATUS = %s"""
              cursor.execute(query, [userID,"Not Recieved"])
              return cursor.fetchall()

The second method selects rows with the value of equal to "Received" for their status attribute.

.. code-block:: python

      def select_drink_oders_user_Received(userID):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """SELECT RESTAURANTS.NAME,DRINKS.NAME,DRINK_ORDERS.PRICE,BUYDATE,STATUS,RESTAURANTS.ID,DRINK_ORDERS.ID
               FROM DRINK_ORDERS,RESTAURANTS,DRINKS WHERE USER_ID = %s AND
              DRINK_ORDERS.REST_ID = RESTAURANTS.ID AND DRINKS.ID = DRINK_ORDERS.DRINK_ID AND DRINK_ORDERS.STATUS = %s"""
              cursor.execute(query, [userID,"Received"])
              return cursor.fetchall()

To list the food orders on user's page these 2 methods were used.

Update
^^^^^^
Drink orders updated from user's profile page. The function given below provokes when the user clicks the "Finish Order" button on the profile page under the list of Unreceived Orders.
As the name implies, it is the user who finishes orders in RESTORANLANDIN. Status column's of orders was set to "Received".

.. code-block:: python

      def update_drink_order_by_id(orderId):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """
              UPDATE DRINK_ORDERS SET
              STATUS = %s
              WHERE (ID = %s)"""
              cursor.execute(statement,["Received",orderId])
              connection.commit()

Delete
^^^^^^
Users may cancel their orders before receiving them. The cancellation process is done by the "Cancel Order" button on the profile page next to "Finish Order" button.
This button provokes the given method below.

.. code-block:: python

      def delete_drink_order_by_id(orderId):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """
              DELETE FROM DRINK_ORDERS WHERE ID = %s"""
              cursor.execute(query, [orderId] )
              connection.commit()


Achievement_User Table
======================

Achievements are the fun part of RESTORANLANDIN. Users can complete achievements with ordering foods.
To keep information about achievements a database table named ACHIEVEMENTS created by Onat Şahin. Connecting achievements with users require another table which named as ACHIEVEMENT_USER.
Mainly this table keeps the record of which user completed which achievement.

Attributes of Achievement_User Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ID SERIAL PRIMARY KEY
    Primary key.
* USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE
    Foreign key refers to the users table.
* ACH_ID INTEGER REFERENCES ACHIEVEMENTS(ID) ON DELETE CASCADE
    Foreign key refers to achievements table.
* USER_ACHIEVED INTEGER NOT NULL
    To keep the number user has so far succeeded.

Operations
^^^^^^^^^^
For this table, 3 operation is enough for the scope of RESTORANLANDIN. These operations are created, update and read.

Create and Update
^^^^^^^^^^^^^^^^^
Inserting rows to Achievement_User table was done by the function given below.
This function also updates the attribute USER_ACHIEVED if there has already been a row for given user with given achievement then this method updates the value.

.. code-block:: python

      def add_row(userId,ach_id):
          currentRow = None
          print(userId,ach_id)
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """SELECT * FROM ACHIEVEMENT_USER WHERE (ACH_ID = %s)
              AND (USER_ID = %s )"""
              cursor.execute(statement,[ach_id,userId])
              currentRow = cursor.fetchone()
          if not currentRow: #There is no information. Insert it to table
              with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  statement = """INSERT INTO ACHIEVEMENT_USER (USER_ACHIEVED,USER_ID,ACH_ID)
                  VALUES (%s,%s,%s)"""
                  cursor.execute(statement,["1",userId,ach_id])
                  #currentRow = cursor.fetchone()
          else: # There is an information update it.
              current = int(currentRow[3])
              current = current+1
              with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  statement = """UPDATE ACHIEVEMENT_USER SET USER_ACHIEVED  =%s WHERE (ACH_ID = %s)
                  AND (USER_ID = %s)"""
                  cursor.execute(statement,[current,ach_id,userId])
                  connection.commit()

This function called inside of the method update_food_order_by_id. After user received a food order, achievements for that food controlled.
 A selection operation was done first. If the return value of it equals to the empty list then a row will be inserted. Else returned row will be updated.


Select
^^^^^^
Selection operation is necessary to list completed achievements in user's profile page. To fetch the information about achievement a join operation was used.

.. code-block:: python

      def select_completed_achievements_by_userID(userId):
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              statement = """SELECT ACHIEVEMENTS.ID,ACHIEVEMENTS.NAME,ACHIEVEMENTS.CONTENT FROM ACHIEVEMENTS,ACHIEVEMENT_USER WHERE (ACH_ID = ACHIEVEMENTS.ID)
              AND (USER_ID = %s ) AND ( USER_ACHIEVED >= ACHIEVEMENTS.GOAL )"""
              cursor.execute(statement,[userId])
              return cursor.fetchall()

A returned value of this function visible on the profile page.
