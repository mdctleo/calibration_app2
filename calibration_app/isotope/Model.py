from app import db
from calibration_app.constants.Constants import *
from sqlalchemy.exc import *
from exceptions.Exceptions import *


class Isotope(db.Model):
    __tablename__ = ISOTOPE_T_NAME
    isotopeName = db.Column(ISOTOPE_C_ISOTOPE_NAME, db.String(8), primary_key=True)
    halfLife = db.Column(ISOTOPE_C_HALF_LIFE, db.Float, nullable=False)
    createdBy = db.Column(ISOTOPE_C_ISOTOPE_CREATED_BY, db.String(100), nullable=False)
    # TODO: Add in relation to user table
    # createdBy = db.Column(db.String(100), db.ForeignKey(USERS_T_NAME + '.' + USERS_C_USERNAME), nullable=False)
    calibrationFactor = db.relationship('CalibrationFactor', backref=ISOTOPE_T_NAME)

    def __init__(self, isotopeName, halfLife, createdBy):
        self.isotopeName = isotopeName
        self.halfLife = halfLife
        self.createdBy = createdBy

    def __repr__(self):
        return '<Isotope %r %r %r >' % (self.isotopeName, self.halfLife, self.createdBy)


class IsotopeSchema(Schema):
    isotopeName = fields.Str()
    halfLife = fields.Float()
    createdBy = fields.String()


class DatabaseHelper:

    @staticmethod
    def getIsotope(name):
        try:
            result = Isotope.query.filter_by(isotopeName=name).first()
        except SQLAlchemyError:
            raise BaseException("Server Error")

        if result is None:
            raise NotFoundException("Isotope not found")

        return result

    @staticmethod
    def getIsotopes():
        try:
            result = Isotope.query.all()
        except SQLAlchemyError:
            raise BaseException("Server Errror")

        return result

    @staticmethod
    def createIsotope(isotope):
        db.session.add(isotope)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            db.session.remove()
            raise IntegrityException("Isotope already in Database or User DNE")
        except SQLAlchemyError:
            db.session.rollback()
            db.session.remove()
            raise BaseException("Server Error")

        return True

    @staticmethod
    def updateIsotope(isotopeToUpdate, newIsotope, createdBy):
        isotopeToUpdate.isotopeName = newIsotope.isotopeName
        isotopeToUpdate.halfLife = newIsotope.halfLife
        isotopeToUpdate.createdBy = createdBy

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            db.session.remove()
            raise IntegrityException("Isotope already in Database or User DNE")
        except SQLAlchemyError:
            db.session.rollback()
            db.session.remove()
            raise BaseException("Server Error")

        return True

    @staticmethod
    def deleteIsotope(isotopeToDelete):
        db.session.delete(isotopeToDelete)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            db.session.remove()
            raise BaseException("Server Error")


