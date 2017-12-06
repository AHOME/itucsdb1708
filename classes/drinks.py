import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin

#dr =  Drinks(select = sel)

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
