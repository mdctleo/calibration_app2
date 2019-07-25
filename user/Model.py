from sqlalchemy.exc import SQLAlchemyError
from exceptions.Exceptions import *

from app import db
from marshmallow import Schema, fields


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

class DatabaseHelper:

    @staticmethod
    def getUser(email):
        try:
            result = User.query.filter_by(email=email).first()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return result

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    token = fields.Str()