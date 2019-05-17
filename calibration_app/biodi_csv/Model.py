from app import db
from calibration_app.constants.Constants import *
from sqlalchemy.exc import *
from exceptions.Exceptions import *

class Protocol(db.Model):
    __tablename__ = PROTOCOL_T_NAME
    id = db.Column(PROTOCOL_C_ID, db.Integer, primary_key=True)
    name = db.Column(PROTOCOL_C_NAME, db.String(8), nullable=False)
    biodiCsv = db.relationship('BiodiCsv', backref=PROTOCOL_T_NAME)

class BiodiCsv(db.Model):
    __tablename__ = BIODI_CSV_T_NAME
    id = db.Column(BIODI_CSV_C_ID, db.Integer, primary_key=True)
    fileName = db.Column(BIODI_CSV_C_FILE_NAME, db.String(45), nullable=False)
    protocolId = db.Column(BIODI_CSV_C_PROTOCOL_ID, db.Integer, nullable=False)

class BiodiCsvValues(db.Model):
    __tablename__ = BIODI_CSV_VALUES_T_NAME
    csvId = db.Column(BIODI_CSV_VALUES_C_CSV_ID, db.Integer, nullable=False)



    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __repr__(self):
        return '<Csv %r %r>' % (self.name, self.data)

class DatabaseHelper:

    @staticmethod
    def getCsvs():
        try:
            result = BiodiCsv.query.all()
        except SQLAlchemyError:
            raise BaseException("Server Errror")

        return result

    @staticmethod
    def createCsvs(csvs):
        for csv in csvs:
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