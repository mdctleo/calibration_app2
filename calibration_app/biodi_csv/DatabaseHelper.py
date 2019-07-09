from app import db
from calibration_app.biodi_csv.BiodiCsvModel import BiodiCsvRow, Protocol
from calibration_app.biodi_csv.BiodiCsvCompleteModel import StudyInformation
from sqlalchemy.exc import *
from exceptions.Exceptions import *

class DatabaseHelper:


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
    def getBiodiCsvMetas():
        try:
            result = StudyInformation.query.with_entities(StudyInformation.id, StudyInformation.studyName, StudyInformation.createdBy, StudyInformation.createdOn).all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return result

    @staticmethod
    def createStudyInformation(studyInformation):
        db.session.add(studyInformation)
        csvId = db.session.flush()

        return csvId

    @staticmethod
    def createBiodiCsvRows(biodiCsvRows):
        for row in biodiCsvRows:
            db.session.add(row)

        return True


    @staticmethod
    def createBiodiCsvCompleteRows(biodiCsvCompleteRows):
        for row in biodiCsvCompleteRows:
            db.session.add(row)

        return True

    @staticmethod
    def createMice(mice):
        for mouse in mice:
            db.session.add(mouse)

    @staticmethod
    def executeCreateStudy():
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.remove()
            raise BaseException(e.__str__())
