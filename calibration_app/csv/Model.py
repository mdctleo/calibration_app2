from app import db
from calibration_app.constants.Constants import *
from sqlalchemy.exc import *
from exceptions.Exceptions import *

class Csv(db.Model):
    __tablename__ = CSV_T_NAME
    id = db.Column(CSV_C_ID, db.Integer, primary_key=True)
    name = db.Column(CSV_C_NAME, db.String(45))
    data = db.Column(CSV_C_DATA, db.JSON)

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __repr__(self):
        return '<Csv %r %r>' % (self.name, self.data)

class DatabaseHelper:

    @staticmethod
    def getCsvs():
        try:
            result = Csv.query.all()
        except SQLAlchemyError:
            raise BaseException("Server Errror")

        return result

    @staticmethod
    def createCsv(csv):
        db.session.add(csv)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            db.session.remove()
            raise IntegrityException("counter already in database")
        except SQLAlchemyError:
            db.session.rollback()
            db.session.remove()
            raise BaseException("Server Error")

        return True