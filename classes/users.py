import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin

class Users(UserMixin):
    def __init__(self,Id,FirstName,LastName,Mail,Password,Birthdate,City,Gender,UserType,Avatar):
        self.Id = Id
        self.FirstName = FirstName
        self.LastName = LastName
        self.Mail = Mail
        self.Password = Password
        self.Birthdate = Birthdate
        self.City = City
        self.Gender = Gender
        self.UserType = UserType
        self.Avatar = Avatar
        self.active = True
        if UserType == 0:
            self.is_admin = True
        else:
            self.is_admin = False

    def get_mail(self):
        return self.Mail


    def get_name(self):
        return self.FirstName

    def get_lastname(self):
        return self.LastName

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    
    def get_id(self):
        return self.Mail

    def get_Id(self):
        return self.Id

def get_user(db_mail):
    if db_mail == 1:
        return None
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM USERS WHERE MAIL = %s"""
        cursor.execute(statement, [db_mail])
        db_user = cursor.fetchall()
        user = Users(db_user[0][0],db_user[0][1], db_user[0][2], db_user[0][3],db_user[0][4], db_user[0][5], db_user[0][6], db_user[0][7], db_user[0][8], db_user[0][9])

    if user is not None:
        user.is_admin = user.Mail in current_app.config['ADMIN_USERS']
    return user