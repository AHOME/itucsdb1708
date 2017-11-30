import psycopg2 as dbapi2
from flask import current_app

class Users:
    def __init__(self,Id,FirstName,LastName,Mail,Password,Birthdate,Bio,City,Gender,UserType,Avatar):
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
