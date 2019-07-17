from app import db
from calibration_app.biodi_csv.Model import StudyInformation, Vector, Organ, BiodiCsvRow, Protocol, Window
from sqlalchemy.exc import *
from exceptions.Exceptions import *

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
            completeStudy = StudyInformation.query.filter(StudyInformation.id == studyId).first()
            windowsCount = Window.query.with_entities(Window.id).filter(Window.csvId == studyId).group_by(Window.isotopeName).count()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return completeStudy, windowsCount


    @staticmethod
    def getBiodiCsvMetas():
        try:
            result = StudyInformation.query.with_entities(StudyInformation.id,
                                                          StudyInformation.studyName,
                                                          StudyInformation.researcherName,
                                                          StudyInformation.createdOn).all()
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
