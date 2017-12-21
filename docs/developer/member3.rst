Parts Implemented by Sadık Ekin Özbay
=====================================
I did CRUD operations of Restaurants, Comments and Foods. Moreover I did create function of order.

Restaurants Table
---------------------------------
Restaurants are the main part of our project.

Attributes of Restaurants Table
^^^^^^^^^^^^^^^^^^^^^^^^^^

* ID SERIAL PRIMARY KEY
    Primary key of restaurants.
* NAME VARCHAR(80) NOT NULL
    Name of the restaurant.
* ADDRESS VARCHAR(255) NOT NULL
    Address of the restaurant.
* CONTACT_NAME VARCHAR(80) NOT NULL
    Contact name of the restaurant.
* CREATOR_ID INTEGER REFERENCES USERS(ID)
    Person who created the restaurant. It is also a reference to users.
* SCORE INTEGER NOT NULL DEFAULT 0 CHECK( SCORE >= 0 AND SCORE <= 5),
    Score of the restaurant. It have to be bigger than 0 and smaller than 5.
* PROFILE_PICTURE VARCHAR(500) NOT NULL,
    It is profile picture link for the restaurant.
* HOURS VARCHAR(80) NOT NULL,
    It is working hours of the restaurant.
* CURRENT_STATUS VARCHAR(80) NOT NULL
    It is current status of the restaurant.

Operations
^^^^^^^^^^
To operate create, select, update and delete operations a class implemented. Class structure is used.
.. code-block:: python
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

Create
^^^^^^
To add new restaurant, create_restaurant method of Restaurant class used. This constructor takes form and current user ID.

.. code-block:: python
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

Edit
^^^^^^
To edit a restaurant, update_restaurant_by_id method of Restaurant class used. This constructor takes form, restaurant ID and current user ID.

.. code-block:: python
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

Delete
^^^^^^
To delete a restaurant, edit_restaurant method of Restaurant class used. This constructor takes only restaurant ID.

.. code-block:: python
  def delete_restaurant_by_id(self, r_id):
      with dbapi2.connect(current_app.config['dsn']) as connection:
          cursor = connection.cursor()
          query = """DELETE FROM RESTAURANTS WHERE ID = %s"""
          cursor.execute(query, [r_id])
          connection.commit()

Select One
^^^^^^^^^^
This method is used for selecting just one spesific restaurant from all restaurants. This method is used in Restaurant show page.

.. code-block:: python
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
          self.contactName =  selectedRestaurant[4]
          self.creatorId =  selectedRestaurant[4]
          self.score =  selectedRestaurant[5]
          self.profilePicture =  selectedRestaurant[6]
          self.hours =  selectedRestaurant[7]
          self.currentStatus =  selectedRestaurant[8]

Select All
^^^^^^^^^^
This method is used for selecting all restaurants.This method is used in Restaurant index page.

.. code-block:: python
  def select_all_restaurants(self):
      with dbapi2.connect(current_app.config['dsn']) as connection:
          cursor = connection.cursor()
          query = """SELECT * FROM RESTAURANTS"""
          cursor.execute(query)
          restaurants = cursor.fetchall()
      return restaurants

Give Star To A Restaurant
^^^^^^^^^^^^^^^^^^^^^^^^^^^
This method allows the users to give ratings to restaurants. The second function checks if the user gave a rating to that restaurant or not. It s/he is not, then s/he can give a rating.

.. code-block:: python
  def give_star_by_id(self, user_id, restaurant_id , score):
      with dbapi2.connect(current_app.config['dsn']) as connection:
          cursor = connection.cursor()
          query = """SELECT * FROM STAR_RESTAURANTS WHERE USER_ID = %s AND RESTAURANT_ID = %s"""
          cursor.execute(query,(user_id,restaurant_id))
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
.. code-block:: python
  def check_user_gave_a_star_or_not(self, user_id, restaurant_id):
      with dbapi2.connect(current_app.config['dsn']) as connection:
          cursor = connection.cursor()
          query = """SELECT * FROM STAR_RESTAURANTS WHERE USER_ID = %s AND RESTAURANT_ID = %s"""
          cursor.execute(query,(user_id,restaurant_id))
          users = cursor.fetchall()
      if(users == []):
          return True
      return False

Foods Table
---------------------------------
Foods are the main part of the Restaurants. We can add foods to restaurants.

Attributes of Foods Table
^^^^^^^^^^^^^^^^^^^^^^^^^^

* ID SERIAL PRIMARY KEY
    Primary key of foods.
* NAME VARCHAR(80) NOT NULL
    Name of the foods.
* ICON VARCHAR(255) NOT NULL
    Icon of the fo0ds.
* FOOD_TYPE VARCHAR(80) NOT NULL
    Type name of the foods.
* PRICE VARCHAR(80) NOT NULL
    Price of the foods.
* CALORIE VARCHAR(80) NOT NULL
    Calorie of the foods.


Operations
^^^^^^^^^^
To operate create, select, update and delete operations a class implemented. Class structure is used.
.. code-block:: python
  class Foods():
      def __init__(self):
          self.primaryId = ""
          self.name = ""
          self.icon = ""
          self.foodType = ""
          self.price = ""
          self.calori = ""

Create
^^^^^^
To add new food, create_food method of Food class used. This constructor takes form.

.. code-block:: python
  def create_food(self, form):

      nameInput = form['name']
      iconInput = form['icon']
      typeNameInput = form['type']
      priceInput = form['price']
      calorieInput = form['calorie']
      with dbapi2.connect(current_app.config['dsn']) as connection:
          cursor = connection.cursor()
          query = """
              INSERT INTO FOODS (NAME, ICON, FOOD_TYPE, PRICE, CALORIE)
              VALUES (%s,%s,%s,%s,%s)"""
          cursor.execute(query, [nameInput, iconInput, typeNameInput, priceInput, calorieInput])
          connection.commit()


Edit
^^^^
To edit a food, food_edit_page is used.

.. code-block:: python
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

Delete
^^^^^^
To delete a food, food_delete_func method is used.

.. code-block:: python
  def food_delete_func(food_id,restaurant_id):
      if current_user.is_admin or current_user.get_type == 1:
          with dbapi2.connect(current_app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """DELETE FROM FOODS WHERE ID = %s"""
              cursor.execute(query, [food_id])
              connection.commit()
      return redirect(url_for('site.food_home_page',restaurant_id = restaurant_id))

Select All
^^^^^^^^^^
This method is used for selecting all foods.This method is used in add food to the restaurant page.

.. code-block:: python
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM FOODS"""
        cursor.execute(query)
        foods = cursor.fetchall()
    return foods


Restaurant_Foods Table
---------------------------------
This is the connection table for restaurants and foods.

Attributes of Restaurant_Foods Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ID SERIAL PRIMARY KEY
    Primary key of restaurant foods.
* RESTAURANT_ID INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE
    Reference to the restaurant.
* FOOD_ID INTEGER REFERENCES FOODS(ID) ON DELETE CASCADE
    Referece to foods.
* SELL_COUNT INTEGER NOT NULL
    Sell count of spesific food on spesific restaurant.


Operations
^^^^^^^^^^
To operate create. Class structure is used.
.. code-block:: python
  class RestaurantFoods():
      def __init__(self, primaryId, restaurantId, foodId):
          self.primaryId = primaryId
          self.restaurantId = restaurantId
          self.foodId = foodId

Create
^^^^^^
To add new food to the spesific restaurant, we use this. Implemented the food part. My friend, Burak Bekci, implemented drink part.

.. code-block:: python
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

Comments Table
---------------------------------
Comments are the one of the main part for restaurants.

Attributes of Comments Table
^^^^^^^^^^^^^^^^^^^^^^^^^^

* ID SERIAL PRIMARY KEY
    Primary key of the comment.
* USER_ID INTEGER REFERENCES USERS(ID) ON DELETE CASCADE
    Reference to the user.
* RESTAURANT_ID INTEGER REFERENCES RESTAURANTS(ID) ON DELETE CASCADE
    Reference of the restaurant.
* CONTENT VARCHAR(255) NOT NULL
    Content of the comment
* SENDDATE TIMESTAMP NOT NULL
    Send date of the comment


Operations
^^^^^^^^^^
To operate create, delete and select operations a class implemented.

Create
^^^^^^
To create new comment, we take content of the comment from user. We take id of the user and id of the current user automaticly.

.. code-block:: python
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
Delete
^^^^^^
Only admin user can delete the comment.

.. code-block:: python
  def delete_comment_by_id(self, c_id):
      with dbapi2.connect(current_app.config['dsn']) as connection:
          cursor = connection.cursor()
          query = """DELETE FROM COMMENTS WHERE ID = %s"""
          cursor.execute(query, [c_id])
          connection.commit()

Select All
^^^^^^^^^^
This method is used for selecting all comments.This method is used in Restaurant show page for showing the comments.

.. code-block:: python
  def select_all_comments(self, restaurantId):
      with dbapi2.connect(current_app.config['dsn']) as connection:
          cursor = connection.cursor()
          query = """SELECT * FROM COMMENTS AS x JOIN USERS AS y ON x.USER_ID = y.ID WHERE RESTAURANT_ID = %s"""
          cursor.execute(query, [restaurantId])
          comments = cursor.fetchall()
      return comments
