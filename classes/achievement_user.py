import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context



def add_row(userId,ach_id):
    currentRow = None
    print(userId,ach_id)
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM ACHIEVEMENT_USER WHERE (ACH_ID = %s)
        AND (USER_ID = %s )"""
        cursor.execute(statement,[ach_id,userId])
        currentRow = cursor.fetchone()
    print("Current Row: ",currentRow)
    if not currentRow: #There is no information. Insert it to table
        print("If happened")
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO ACHIEVEMENT_USER (USER_ACHIEVED,USER_ID,ACH_ID)
            VALUES (%s,%s,%s)"""
            cursor.execute(statement,["1",userId,ach_id])
            #currentRow = cursor.fetchone()
    else: # There is an information update it.
        print("Else happened")
        current = int(currentRow[3])
        current = current+1
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """UPDATE ACHIEVEMENT_USER SET USER_ACHIEVED  =%s WHERE (ACH_ID = %s)
            AND (USER_ID = %s)"""
            cursor.execute(statement,[current,ach_id,userId])
            connection.commit()
def select_completed_achievements_by_userID(userId):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT ACHIEVEMENTS.ID,ACHIEVEMENTS.NAME,ACHIEVEMENTS.CONTENT FROM ACHIEVEMENTS,ACHIEVEMENT_USER WHERE (ACH_ID = ACHIEVEMENTS.ID)
        AND (USER_ID = %s ) AND ( USER_ACHIEVED >= ACHIEVEMENTS.GOAL )"""
        cursor.execute(statement,[userId])
        return cursor.fetchall()
