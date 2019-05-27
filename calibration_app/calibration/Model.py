from app import db
from calibration_app.constants.Constants import *
import datetime
from exceptions.Exceptions import *
from sqlalchemy.exc import *


class CalibrationFactor(db.Model):
    __tablename__ = CALIBRATION_T_NAME
    id = db.Column(CALIBRATION_C_ID, db.Integer, primary_key=True)
    factor = db.Column(CALIBRATION_C_FACTOR, db.Float)
    createdOn = db.Column(CALIBRATION_C_CREATED_ON, db.TIMESTAMP, default=datetime.datetime.utcnow)
    isotopeName = db.Column(CALIBRATION_C_ISOTOPE_NAME, db.String(8),
                            db.ForeignKey(ISOTOPE_T_NAME + '.' + ISOTOPE_C_ISOTOPE_NAME))
    createdBy = db.Column(CALIBRATION_C_CREATED_BY, db.String(100), nullable=False)
    gammaCounter = db.Column(CALIBRATION_C_GAMMA_COUNTER, db.String(100),
                             db.ForeignKey(GAMMA_COUNTERS_T_NAME + '.' +  GAMMA_COUNTERS_C_MODEL), nullable=False)
    # TODO: Add in relation to User table
    # createdBy = db.Column(CALIBRATION_C_CREATED_BY, db.String(100),
    #                       db.ForeignKey(USERS_T_NAME + '.' + USERS_C_USERNAME))

    def __init__(self, factor, isotopeName, createdOn, createdBy, gammaCounter):
        self.factor = factor
        self.isotopeName = isotopeName
        self.createdOn = createdOn
        self.createdBy = createdBy
        self.gammaCounter = gammaCounter

    def __repr__(self):
        return '<CalibrationFactor %r %r %r %r %r %r>' % (self.id, self.factor, self.isotopeName, self.createdOn, self.createdBy, self.gammaCounter)
        # from calibration_app.calibration.Model import CalibrationFactor
        # u = CalibrationFactor(id= , factor= , isotopeName= , createdOn= , createdBy= , gammaCounter= )

class CalibrationFactorSchema(Schema):
    id = fields.Integer()
    factor = fields.Float()
    createdOn = fields.DateTime()
    isotopeName = fields.String()
    createdBy = fields.String()
    gammaCounter = fields.String()


class CalibrationFactorGraphSchema(Schema):
    createdOns = fields.List(fields.DateTime())
    factors = fields.List(fields.Float())



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
    def getCalibrationFactors(model, isotopeName):
        try:
            filters = []

            if model is not None:
                filters.append(CalibrationFactor.gammaCounter == model)

            if isotopeName is not None:
                filters.append(CalibrationFactor.isotopeName == isotopeName)

            result = CalibrationFactor.query.filter(*filters).all()

        except SQLAlchemyError:
            raise BaseException("Server Errror")

        return result

    @staticmethod
    def createCalibrationFactor(calibrationFactor):
        db.session.add(calibrationFactor)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            db.session.remove()
            raise IntegrityException("Integrity Constraints from Database")
        except SQLAlchemyError:
            db.session.rollback()
            db.session.remove()
            raise BaseException("Server Error")

        return True

    @staticmethod
    def getCalibrationFactorsGraph(model, isotopeName):
        try:
            filters = []

            if model is not None:
                filters.append(CalibrationFactor.gammaCounter == model)

            if isotopeName is not None:
                filters.append(CalibrationFactor.isotopeName == isotopeName)

            result = CalibrationFactor.query.filter(*filters)\
                .order_by(CalibrationFactor.createdOn).all()

        except SQLAlchemyError:
            raise BaseException("Server Errror")

        return result


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