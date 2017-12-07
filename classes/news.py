import psycopg2 as dbapi2
from flask import current_app


class News():
    def __init__(self,Topic,Content,Link,Restaurant):
        self.Id = ''
        self.Topic = Topic
        self.Content = Content
        self.Link = Link
        self.Restaurant = Restaurant

    def find_news_id(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT ID FROM NEWS WHERE TOPIC = %s AND CONTENT = %s"""
            cursor.execute(query, (self.Topic,self.Content))
            db_news = cursor.fetchone()
        self.Id =db_news[0]

    def insert_news(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            if self.Restaurant == "":
                statement = """
                INSERT INTO NEWS (TOPIC, CONTENT, LINK )
                VALUES (%s,%s,%s)"""
                cursor.execute(statement,(self.Topic,self.Content,self.Link))
            else:
                statement = """
                INSERT INTO NEWS (TOPIC, CONTENT, LINK , RESTAURANT)
                VALUES (%s,%s,%s,%s)"""
                cursor.execute(statement,(self.Topic,self.Content,self.Link,self.Restaurant))

            connection.commit()
    
    def update_news(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            if self.Restaurant == "":
                query = """UPDATE NEWS SET TOPIC = %s, CONTENT = %s, LINK = %s"""
                cursor.execute(query,(self.Topic,self.Content,self.Link))
            else:
                query = """UPDATE NEWS SET TOPIC = %s, CONTENT = %s, LINK = %s, RESTAURANT = %s"""
                cursor.execute(query,(self.Topic,self.Content,self.Link,self.Restaurant))
            connection.commit()
    

def delete_news(Id):
        if Id != '':
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """DELETE FROM NEWS WHERE ID = %s"""
                cursor.execute(statement, [Id])
                connection.commit()
    

def get_news_by_id(id):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
        SELECT * FROM NEWS WHERE ID = %s"""
        cursor.execute(query,[id])
        db_news = cursor.fetchone()
        news_class = News(db_news[1],db_news[2],db_news[3],db_news[4])
        news_class.find_news_id()
        return news_class



def get_all_news():
    with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM NEWS"""
            cursor.execute(query)
            db_news = cursor.fetchall()
            if db_news is None:
                db_news = {}
            return db_news