from app import db
from calibration_app.biodi_csv.Model import StudyInformation, Vector, Organ, BiodiCsvRow, Protocol, Window, Chelator, CellLine, MouseStrain, TumorModel
from sqlalchemy.exc import *

from calibration_app.calibration.Model import CalibrationFactor
from calibration_app.isotope.Model import Isotope
from exceptions.Exceptions import *
import pandas as pd

class DatabaseHelper:

    @staticmethod
    def getDb():
        return db


    @staticmethod
    def getBiodiCsv(csvId):
        try:
            fileName = db.session.query(StudyInformation).with_entities(StudyInformation.studyName).filter(StudyInformation.id == csvId).first()
            csvRows = db.session.query(StudyInformation, BiodiCsvRow, Protocol) \
                .with_entities(
                Protocol.id,
                Protocol.protocolName,
                BiodiCsvRow.measurementTime,
                BiodiCsvRow.completionStatus,
                BiodiCsvRow.runId,
                BiodiCsvRow.rack,
                BiodiCsvRow.det,
                BiodiCsvRow.pos,
                BiodiCsvRow.time,
                BiodiCsvRow.sampleCode,
                BiodiCsvRow.counts,
                BiodiCsvRow.cpm,
                BiodiCsvRow.error,
                BiodiCsvRow.info) \
                .filter(StudyInformation.id == csvId) \
                .filter(BiodiCsvRow.csvId == StudyInformation.id) \
                .filter(Protocol.id == StudyInformation.protocolId) \
                .order_by(BiodiCsvRow.rowNum).all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())
        return fileName, csvRows

    @staticmethod
    def getCompleteStudy(studyId):
        try:
            result = db.session.query(StudyInformation, Isotope, CalibrationFactor) \
            .outerjoin(CalibrationFactor, CalibrationFactor.isotopeName == StudyInformation.isotopeName and CalibrationFactor.gammaCounter == StudyInformation.gammaCounter) \
            .filter(StudyInformation.id == studyId) \
            .filter(Isotope.isotopeName == StudyInformation.isotopeName) \
            .order_by(CalibrationFactor.createdOn.desc()).first()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())
        completeStudy = result[0]
        isotope = result[1]
        calibrationFactor = 1 if result[2] is None else result[2].factor
        return completeStudy, isotope, calibrationFactor

    @staticmethod
    def getBiodiCsvRaw(studyId):
        try:
            completeStudy = StudyInformation.query.filter(StudyInformation.id == studyId).first()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return completeStudy


    @staticmethod
    def getBiodiCsvMetas():
        try:
            result = StudyInformation.query.with_entities(StudyInformation.id,
                                                          StudyInformation.studyName,
                                                          StudyInformation.studyDate,
                                                          StudyInformation.researcherName,
                                                          StudyInformation.piName,
                                                          StudyInformation.isotopeName,
                                                          StudyInformation.chelatorName,
                                                          StudyInformation.vectorName,
                                                          StudyInformation.target,
                                                          StudyInformation.cellLineName,
                                                          StudyInformation.tumorModelName,
                                                          StudyInformation.mouseStrainName,
                                                          StudyInformation.gammaCounter).all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return result

    @staticmethod
    def createStudy(study):
        try:
            db.session.add(study)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.remove()
            raise BaseException(e.__str__())


    @staticmethod
    def getOrgan(organName):
        try:
            organ = Organ.query.filter_by(name=organName).first()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return organ

    @staticmethod
    def getVector(vectorName):
        try:
            vector = Vector.query.filter_by(name=vectorName).first()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return vector

    @staticmethod
    def getProtocolName(protocolId):
        try:
            protocolName = Protocol.query.filter_by(id=protocolId).first().protocolName
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return protocolName

    @staticmethod
    def getChelators():
        try:
            chelators = Chelator.query.all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return chelators

    @staticmethod
    def getVectors():
        try:
            vectors = Vector.query.all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return vectors

    @staticmethod
    def getCellLines():
        try:
            cellLines = CellLine.query.all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return cellLines

    @staticmethod
    def getMouseStrains():
        try:
            mouseStrains = MouseStrain.query.all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return mouseStrains

    @staticmethod
    def getTumorModels():
        try:
            tumorModels = TumorModel.query.all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return tumorModels
