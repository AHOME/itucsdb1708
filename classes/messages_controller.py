import psycopg2 as dbapi2
from flask import current_app
from flask import request,flash,session

def select_all_messages(user_id):

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM MESSAGES WHERE SENDER = %s OR RECEIVER = %s"""
        cursor.execute(statement,(user_id,user_id))
        messages = cursor.fetchall()
        
    for message in messages:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT FIRSTNAME FROM USERS WHERE ID = (SELECT SENDER FROM MESSAGES WHERE ID = %s)"""
            cursor.execute(statement,[message[0]])
            sender_name =  (cursor.fetchone())[0]

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT LASTNAME FROM USERS WHERE ID = (SELECT SENDER FROM MESSAGES WHERE ID = %s)"""
            cursor.execute(statement,[message[0]])
            sender_name += " " + (cursor.fetchone())[0]

        message = list(message)
        message[1] = sender_name
        message = tuple(message)

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT FIRSTNAME FROM USERS WHERE ID = (SELECT RECEIVER FROM MESSAGES WHERE ID = %s)"""
            cursor.execute(statement,[message[0]])
            receiver_name = (cursor.fetchone())[0]

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT LASTNAME FROM USERS WHERE ID = (SELECT RECEIVER FROM MESSAGES WHERE ID = %s)"""
            cursor.execute(statement,[message[0]])
            receiver_name += " " + (cursor.fetchone())[0]

        message = list(message)
        message[2] = receiver_name
        message = tuple(message)
        
        return messages

def validate_message_data(form):
    if form == None:
        return true

    form.data = {}
    form.errors = {}

    receiver = request.form['message_target']
    sender = session['id']
    topic = request.form['message_topic']
    body = request.form['message_body']

    if len(body) == 0:
        form.errors['message_body'] = 'Message body can not be empty!'
    else:
        form.data['message_body'] = body

    if len(topic) == 0:
        form.errors['message_topic'] = 'Topic body can not be empty!'
    else:
        form.data['message_topic'] = topic

    if len(receiver) == 0:
        form.errors['message_target'] = 'Target  user can not be blank'
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT ID FROM USERS WHERE MAIL = %s"""
                cursor.execute(statement,[receiver])
                receiver_id = cursor.fetchone()
        if receiver_id is None:
            form.errors['message_target'] = 'Target mail is not valid.'
        else:
            form.data['message_target'] = receiver_id

    return len(form.errors) == 0