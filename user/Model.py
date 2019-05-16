# from medphys import db
# from constants.Constants import *
#
# class User(db.Model):
#     __tablename__ = USERS_T_NAME
#     username = db.Column(USERS_C_USERNAME, db.String(100), primary_key=True)
#     password = db.Column(USERS_C_PASSWORD, db.String(200), nullable=False)
#     isotope = db.relationship('Isotope', backref=USERS_T_NAME, lazy=True)
#     calibrationFactor = db.relationship('CalibrationFactor', backref=USERS_T_NAME, lazy=True)
#
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
#
#     def __repr__(self):
#         return '<User %r>' % self.username

from app import db, login
from constants.Constants import *


from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String())

    def __repr__(self):
        return '<User %r %r %r>' % (self.username, self.email, self.password_hash)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
