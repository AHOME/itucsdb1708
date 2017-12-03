import psycopg2 as dbapi2
from flask import current_app
def create_restaurant(form):
    nameInput =  form['Name']
    addressInput =  form['Address']
    contactNameInput =  form['ContanctName']
    contactPhoneInput =  form['ContanctPhone']
    photoInput =  form['Photo']
    workingHoursInput =  form['WorkingHours']
    currentStatusInput =  form['CurrentStatus']
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            INSERT INTO RESTAURANTS (NAME, ADDRESS, CONTACT_NAME, CONTACT_PHONE, PROFILE_PICTURE,HOURS,CURRENT_STATUS)
            VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(query, [nameInput, addressInput, contactNameInput, contactPhoneInput, photoInput, workingHoursInput, currentStatusInput ])
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
    return selectedRestaurant


def delete_restaurant_by_id(Id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """DELETE FROM RESTAURANTS WHERE ID = %s"""
        cursor.execute(query, [restaurant_id])
        connection.commit()


  def update_restaurant_by_id(form,restaurantId):
        nameInput =  form['Name']
        addressInput =  form['Address']
        contactNameInput =  form['ContanctName']
        contactPhoneInput =  form['ContanctPhone']
        photoInput =  form['Photo']
        workingHoursInput =  form['WorkingHours']
        currentStatusInput =  form['CurrentStatus']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE RESTAURANTS SET NAME = %s, ADDRESS = %s, CONTACT_NAME = %s, CONTACT_PHONE = %s, PROFILE_PICTURE = %s, HOURS = %s, CURRENT_STATUS = %s WHERE ID = %s"""
            cursor.execute(query, [nameInput, addressInput, contactNameInput, contactPhoneInput, photoInput, workingHoursInput, currentStatusInput, restaurant_id])
            connection.commit()
