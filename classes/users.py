import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin

class Users(UserMixin):
    def __init__(self,Id,FirstName,LastName,Mail,Password,Birthdate,City,Gender,UserType,Avatar,Bio):
        self.Id = Id
        self.FirstName = FirstName
        self.LastName = LastName
        self.Mail = Mail
        self.Password = Password
        self.Birthdate = Birthdate
        self.Bio = Bio
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
    if type(db_mail) is int:
        return None

    if db_mail in current_app.config['ADMIN_USERS']:
        user = Users(1,'admin','admin','admin@restoranlandin.com',current_app.config['PASSWORD'], '10.10.2012', '', '',0, 'avatar','')
        return user

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM USERS WHERE MAIL = %s"""
        cursor.execute(statement, [db_mail])
        db_user = cursor.fetchone()
        if db_user is None:
            adminuser=Users(1,'admin','admin','admin@restoranlandin.com',current_app.config['PASSWORD'], '10.10.2012', '', '',0, 'avatar','')
            return adminuser
        user = Users(db_user[0],db_user[1], db_user[2], db_user[3],db_user[4], db_user[5], db_user[6], db_user[7], db_user[8], db_user[9], db_user[10])


    if user is not None:
        user.is_admin = user.Mail in current_app.config['ADMIN_USERS']

    return user
