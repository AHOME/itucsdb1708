import psycopg2 as dbapi2
from flask import current_app

class Messages:
    def __init__(self,Id,Sender,Receiver,Topic,Content,SendDate):
        self.Id = Id
        self.Sender = Sender
        self.LastName = LastName
        self.Receiver = Receiver
        self.Topic = Topic
        self.Content = Content
        self.SendDate = SendDate