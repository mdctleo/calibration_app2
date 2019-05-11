from app import db
from calibration_app.constants.Constants import *
from sqlalchemy.exc import *
from exceptions.Exceptions import *

class GammaCounter(db.Model):
    __tablename__ = GAMMA_COUNTERS_T_NAME
    model = db.Column(GAMMA_COUNTERS_C_MODEL,db.String(100), primary_key=True)
    calibrationFactor = db.relationship('CalibrationFactor', backref=GAMMA_COUNTERS_T_NAME)

    def __init__(self, model):
        self.model = model

    def __repr__(self):
        return '<GammaCounter %r>' % (self.model)


class GammaCounterSchema(Schema):
    model = fields.Str()



class DatabaseHelper:

    # @staticmethod
    # def getIsotope(name):
    #     try:
    #         result = Isotope.query.filter_by(isotopeName=name).first()
    #     except SQLAlchemyError:
    #         raise BaseException("Server Error")
    #
    #     if result is None:
    #         raise NotFoundException("Isotope not found")
    #
    #     return result
    #
    @staticmethod
    def getCounters():
        try:
            result = GammaCounter.query.all()
        except SQLAlchemyError:
            raise BaseException("Server Errror")

        return result

    @staticmethod
    def createCounter(counter):
        db.session.add(counter)
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

    # @staticmethod
    # def updateIsotope(isotopeToUpdate, newIsotope, createdBy):
    #     isotopeToUpdate.isotopeName = newIsotope.isotopeName
    #     isotopeToUpdate.halfLife = newIsotope.halfLife
    #     isotopeToUpdate.createdBy = createdBy
    #
    #     try:
    #         db.session.commit()
    #     except IntegrityError:
    #         db.session.rollback()
    #         db.session.remove()
    #         raise IntegrityException("Isotope already in Database or User DNE")
    #     except SQLAlchemyError:
    #         db.session.rollback()
    #         db.session.remove()
    #         raise BaseException("Server Error")
    #
    #     return True
    #
    # @staticmethod
    # def deleteIsotope(isotopeToDelete):
    #     db.session.delete(isotopeToDelete)
    #     try:
    #         db.session.commit()
    #     except SQLAlchemyError:
    #         db.session.rollback()
    #         db.session.remove()
    #         raise BaseException("Server Error")
