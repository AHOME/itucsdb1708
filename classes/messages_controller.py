import psycopg2 as dbapi2
from flask import current_app

def select_all_messages(user_id):

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM MESSAGES WHERE SENDER = %s OR RECEIVER = %s"""
        cursor.execute(statement,(user_id,user_id))
        messages = cursor.fetchall()
        
        return messages

def validate_message_data(form):
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