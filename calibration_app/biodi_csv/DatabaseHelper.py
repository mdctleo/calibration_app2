from app import db
from calibration_app.biodi_csv.BiodiCsvModel import BiodiCsv, BiodiCsvRow, Protocol
from calibration_app.biodi_csv.BiodiCsvCompleteModel import BiodiCsvComplete
from sqlalchemy.exc import *
from exceptions.Exceptions import *

class DatabaseHelper:

    @staticmethod
    def createBiodiCsvRows(biodiCsvRows):
        for row in biodiCsvRows:
            db.session.add(row)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.remove()
            raise BaseException(e.__str__())

        return True

    @staticmethod
    def getBiodiCsv(csvId):
        try:
            fileName = db.session.query(BiodiCsv).with_entities(BiodiCsv.fileName).filter(BiodiCsv.id == csvId).first()
            csvRows = db.session.query(BiodiCsv, BiodiCsvRow, Protocol) \
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
                .filter(BiodiCsv.id == csvId) \
                .filter(BiodiCsvRow.csvId == BiodiCsv.id) \
                .filter(Protocol.id == BiodiCsv.protocolId) \
                .order_by(BiodiCsvRow.rowNum).all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())
        return fileName, csvRows

    @staticmethod
    def createBiodiCsv(meta):
        db.session.add(meta)
        try:
            db.session.commit()
            csvId = meta.id
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.remove()
            raise BaseException(e.__str__())

        return csvId

    @staticmethod
    def getBiodiCsvMetas():
        try:
            result = BiodiCsv.query.with_entities(BiodiCsv.id, BiodiCsv.fileName, BiodiCsv.createdBy, BiodiCsv.createdOn).all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return result

    @staticmethod
    def createBiodiCsvComplete(meta):
        db.session.add(meta)
        try:
            db.session.commit()
            csvId = meta.id
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.remove()
            raise BaseException(e.__str__())

        return csvId

    @staticmethod
    def createBiodiCsvComplete(biodiCsvCompleteRows):
        for row in biodiCsvCompleteRows:
            db.session.add(row)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())


        return True
