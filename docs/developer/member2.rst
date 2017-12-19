Parts Implemented by Onat Şahin
===============================

Deals and achievements are implemented. Tables, classes and functions required to make database operations are created.
Additionally, the functionality of the search bar is implemented. All of these is also connected to the frontend.

Achievements Table, Class & Functions
-------------------------------------
Achievements are created by the admin and makes ordering from site more enjoyable.

Attributes of Achievements Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ID SERIAL PRIMARY KEY
    Primary key of achievements
* NAME VARCHAR(80) NOT NULL
    Name of the achievement
* ICON VARCHAR(255) NOT NULL
    Icon of the achievement
* CONTENT VARCHAR(80) NOT NULL
    Detailed information about the achievement
* GOAL INTEGER NOT NULL
    The amount of the item needed to unlock the achievemeny
* ENDDATE DATE NOT NULL
    Last day in which the achievement is available

Achievement Creation
^^^^^^^^^^^^^^^^^^^^
To implement the achievement operations, I created a class for achievements. I use the constructor of this class to create
achievements. The constructor either uses the output of a select statement or uses input entered by user to the achievement
creation form.

.. code-block:: python

        def __init__(self,form = None,select = None):
            if form is None:
                self.Id = select[0]
                self.name = select[1]
                self.icon = select[2]
                self.content = select[3]
                self.goal = select[4]
                self.endDate = select[5]
            elif select is None:
                self.Id = ""
                self.name = form['Name']
                self.icon = form['Icon']
                self.content = form['Explanation']
                self.goal = form['Goal']
                self.endDate = form['endDate']

                with dbapi2.connect(current_app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """
                        INSERT INTO ACHIEVEMENTS (NAME, ICON, CONTENT, GOAL, ENDDATE)
                        VALUES (%s,%s,%s,%s,%s)"""
                    cursor.execute(query, (self.name, self.icon, self.content, self.goal, self.endDate))
                    connection.commit()
                with dbapi2.connect(current_app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    statement = """SELECT * FROM ACHIEVEMENTS WHERE (NAME = %s)
                    AND (ICON = %s)
                    AND (CONTENT = %s)
                    AND (GOAL = %s)
                    AND (ENDDATE = %s)"""
                    cursor.execute(statement,[self.name,self.icon, self.content, self.goal, self.endDate])
                    IdofCurrent = cursor.fetchone()[0]
                    self.Id = IdofCurrent

Achievement Selection
^^^^^^^^^^^^^^^^^^^^^
Two different functions are used to select achievements from the database

.. code-block:: python

        def achievement_select_by_Id(Id):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT * FROM ACHIEVEMENTS WHERE (ID = %s)"""
                cursor.execute(statement,[Id])
                return cursor.fetchone()

This first function selects a user by its id. This function is used in the achievement show page.

.. code-block:: python

        def achievement_select_all():
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """SELECT * FROM ACHIEVEMENTS"""
                cursor.execute(query)
                return cursor.fetchall()

This second function returns all achievements. It is used in the admin page to list all achievements.

Achievement Deletion
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

        def achievement_delete_by_Id(Id):
            query = """DELETE FROM ACHIEVEMENTS WHERE ID = %s"""
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute(query, [Id])
                connection.commit()

This function deletes an achievement from the database using its id. It is used in the admin page function to allow the admin to delete
achievements

Achievement Update
^^^^^^^^^^^^^^^^^^

.. code-block:: python

        def achievement_update(form, achievement_id):
            name = form['Name']
            content = form['Explanation']
            goal = form['Goal']
            endDate = form['endDate']
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """UPDATE ACHIEVEMENTS SET NAME=%s, CONTENT=%s, GOAL=%s, ENDDATE=%s  WHERE (ID = %s)"""
                cursor.execute(statement,[name, content, goal, endDate, achievement_id])
                connection.commit()

This function is used in the achievement show page to update the achievement shown on the page. Inputs are taken from the form.


Deals Table, Class & Functions
-------------------------------------
Deals are created by the restaurant owners. It is an essential part of our site.

Attributes of Deals Table
^^^^^^^^^^^^^^^^^^^^^^^^^

* ID SERIAL PRIMARY KEY,
    Primary key of deals
* FOOD_ID INTEGER REFERENCES FOODS(ID) ON DELETE CASCADE,
    Foreign key that references the Foods table to choose which food the deal is for.
* REST_ID INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE,
    Foreign key that references the Restaurants table to specify which restaurant the deal belongs to.
* DATE DATE NOT NULL,
    Final date of the deal.
* DISCOUNT_RATE INTEGER NOT NULL CHECK(DISCOUNT_RATE >= 0 AND DISCOUNT_RATE <= 100)
    Discount rate which takes a value between 0 and 100.

Deal Creation
^^^^^^^^^^^^^
To implement the deal operations, I created a class for deals. I use the constructor of this class to create
deals. The constructor either uses the output of a select statement or uses input entered by user by clicking
"Add Deal" button of an item and entering needed information to the deal creation form.

.. code-block:: python

        def __init__(self, select=None, form=None, foodId=None, restaurantId=None):
            if form is None:
                self.primaryId = select[0]
                self.foodId = select[1]
                self.restaurantId = select[2]
                self.date = select[3]
                self.discountRate = select[4]
            else:
                self.foodId = foodId
                self.restaurantId = restaurantId
                self.date = form['ValidDate']
                self.discountRate = form['rate']

                with dbapi2.connect(current_app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """
                        INSERT INTO DEALS (FOOD_ID, REST_ID, DATE, DISCOUNT_RATE)
                        VALUES (%s,%s,%s,%s)"""
                    cursor.execute(query, [self.foodId, self.restaurantId, self.date, self.discountRate])
                    connection.commit()
                with dbapi2.connect(current_app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    statement = """SELECT * FROM DEALS WHERE (FOOD_ID = %s)
                    AND (REST_ID = %s)
                    AND (DATE = %s)
                    AND (DISCOUNT_RATE = %s)"""
                    cursor.execute(statement,[self.foodId, self.restaurantId, self.date, self.discountRate])
                    IdofCurrent = cursor.fetchone()[0]
                    self.primaryId = IdofCurrent

Deal Selection
^^^^^^^^^^^^^^
Two different functions are used to select deals.

.. code-block:: python

        def select_deals_of_restaurant(restaurantId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT FOODS.NAME, DEALS.DISCOUNT_RATE, FOODS.PRICE, DEALS.ID FROM FOODS, DEALS, RESTAURANT_FOODS
                    WHERE FOODS.ID = DEALS.FOOD_ID AND RESTAURANT_FOODS.RESTAURANT_ID = %s AND RESTAURANT_FOODS.FOOD_ID = DEALS.FOOD_ID
                    AND DEALS.REST_ID = %s"""
                cursor.execute(statement,[restaurantId, restaurantId])
                comers = cursor.fetchall()
                return comers

This function returns every deal in a restaurant. It takes restaurant's id as a parameter. It is used in restaurant
pages to list the deals in that restaurant.

.. code-block:: python

        def select_deal_by_Id(Id):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT * FROM DEALS WHERE (ID = %s)"""
                cursor.execute(statement,[Id])
                return cursor.fetchone()

This function returns the deal for which the id is given. It is used in the deals_update_function to select the deal
to update

Deal Deletion
^^^^^^^^^^^^^
Two different functions are used to delete deals.

.. code-block:: python

        def delete_deals_by_Id(Id):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """
                    DELETE FROM DEALS WHERE ID = %s"""
                cursor.execute(query, [Id])
                connection.commit()

This function is used when a restaurant owners wants to remove a deal from their restaurant's page. According to which deal's
delete button the user pushes, corresponding id is passed to the function as a parameter to delete that deal from the database.

.. code-block:: python

        def delete_unnecessary_rows():
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """
                    DELETE FROM DEALS WHERE REST_ID IS NULL OR
                    FOOD_ID IS NULL"""
                cursor.execute(query)
                connection.commit()

This function is used whenever a food or a restaurant is deleted. It deletes the deals related to deleted restaurants or foods.

Deal Update
^^^^^^^^^^^
.. code-block:: python

    def update_deal_by_Id(form, Id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """
            UPDATE DEALS SET DISCOUNT_RATE = %s, DATE = %s WHERE (ID = %s)"""
            cursor.execute(statement,[form['rate'],form['ValidDate'],Id])
            connection.commit()

This function is used when a restaurant owners wants to update a deal from their restaurant's page. According to which deal's
update button the user pushes, corresponding id and the form are passed to the function as a parameter to update that deal.

The Search Bar
--------------
The home_page_search() function is implemented to allow the users to search for other users or restaurants in the site.
The function uses select statements that includes 'WHERE' and 'LIKE' procedures to find the restaurants and users which
includes the searched word in their names. Then the function redirects to the search results page in which the results
will be shown.

.. code-block:: python

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
