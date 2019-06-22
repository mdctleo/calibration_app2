from app import db
from calibration_app.constants.Constants import *
from sqlalchemy.exc import *
from exceptions.Exceptions import *
import datetime
# from sqlalchemy.dialects.mysql import TINYINT, INTEGER


class Protocol(db.Model):
    __tablename__ = PROTOCOL_T_NAME
    id = db.Column(PROTOCOL_C_ID, db.Integer, primary_key=True, autoincrement=True)
    protocolName = db.Column(PROTOCOL_C_NAME, db.String(8), nullable=False)
    biodiCsv = db.relationship('BiodiCsv', backref=PROTOCOL_T_NAME)

    def __init__(self, protocolName):
        self.protocolName = protocolName

    def __repr__(self):
        return '<Protocol %r %r>' % (self.id, self.name)


class BiodiCsv(db.Model):
    __tablename__ = BIODI_CSV_T_NAME
    id = db.Column(BIODI_CSV_C_ID, db.Integer, primary_key=True, autoincrement=True)
    fileName = db.Column(BIODI_CSV_C_FILE_NAME, db.String(45), nullable=False)
    protocolId = db.Column(BIODI_CSV_C_PROTOCOL_ID, db.Integer, db.ForeignKey(PROTOCOL_T_NAME + '.' + PROTOCOL_C_ID), nullable=False)
    createdOn = db.Column(BIODI_CSV_C_CREATED_ON, db.TIMESTAMP, default=datetime.datetime.utcnow)
    createdBy = db.Column(BIODI_CSV_C_CREATED_BY, db.String(100), nullable=False)
    biodiCsvValues = db.relationship('BiodiCsvRow', cascade="all, delete-orphan", backref=BIODI_CSV_T_NAME)

    def __init__(self, fileName, protocolId, createdBy):
        self.fileName = fileName
        self.protocolId = protocolId
        self.createdBy = createdBy

    def __repr__(self):
        return '<BiodiCsv %r %r %r>' % (self.id, self.fileName, self.protocolId)


class BiodiCsvRow(db.Model):
    __tablename__ = BIODI_CSV_VALUES_T_NAME
    id = db.Column(BIODI_CSV_VALUES_C_ID, db.Integer, primary_key=True, autoincrement=True)
    csvId = db.Column(BIODI_CSV_VALUES_C_CSV_ID, db.Integer, db.ForeignKey(BIODI_CSV_T_NAME + '.' + BIODI_CSV_C_ID), nullable=False)
    rowNum = db.Column(BIODI_CSV_VALUES_C_ROW_NUM, db.Integer, nullable=False)
    measurementTime = db.Column(BIODI_CSV_VALUES_C_MEASUREMENT_DATETIME, db.DateTime)
    completionStatus = db.Column(BIODI_CSV_VALUES_C_COMPLETION_STATUS, db.Integer)
    runId = db.Column(BIODI_CSV_VALUES_C_RUN_ID, db.Integer)
    rack = db.Column(BIODI_CSV_VALUES_C_RACK, db.Integer)
    det = db.Column(BIODI_CSV_VALUES_C_DET, db.Integer)
    pos = db.Column(BIODI_CSV_VALUES_C_POS, db.Integer)
    time = db.Column(BIODI_CSV_VALUES_C_TIME, db.Float)
    sampleCode = db.Column(BIODI_CSV_VALUES_C_SAMPLE_CODE, db.String(45))
    counts = db.Column(BIODI_CSV_VALUES_C_COUNTS, db.Float)
    cpm = db.Column(BIODI_CSV_VALUES_C_CPM, db.Float)
    error = db.Column(BIODI_CSV_VALUES_C_ERROR, db.Float)
    info = db.Column(BIODI_CSV_VALUES_C_INFO, db.CHAR(1))

    def __init__(self, csvId, rowNum, measurementTime, completionStatus, runId,
                 rack, det, pos, time, sampleCode, counts, cpm, error, info):
        self.csvId = csvId
        self.rowNum = rowNum
        self.measurementTime = measurementTime
        self.completionStatus = completionStatus
        self.runId = runId
        self.rack = rack
        self.det = det
        self.pos = pos
        self.time = time
        self.sampleCode = sampleCode
        self.counts = counts
        self.cpm = cpm
        self.error = error
        self.info = info

    # def __repr__(self):
    #     return '<BiodiCsvRow %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r>' % \
    #            (self.id, self.csvId, self.rowNum, self.measurementTime, self.completionStatus,
    #             self.runId, self.rack, self.det, self.pos, self.time, self.sampleCode, self.counts,
    #             self.cpm, self.error, self.info)

    def __repr__(self):
        return '<BiodiCsvRow %r>' % \
               (self.rowNum)


class DatabaseHelper:

    @staticmethod
    def createCsvs(biodiCsvRows):
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
    def getCsv(csvId):
        try:
            fileName = db.session.query(BiodiCsv).with_entities(BiodiCsv.fileName).filter(BiodiCsv.id == csvId).first()
            csvRows = db.session.query(BiodiCsv, BiodiCsvRow, Protocol)\
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
                               BiodiCsvRow.info)\
                .filter(BiodiCsv.id == csvId)\
                .filter(BiodiCsvRow.csvId == BiodiCsv.id)\
                .filter(Protocol.id == BiodiCsv.protocolId)\
                .order_by(BiodiCsvRow.rowNum).all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())
        return fileName, csvRows

    @staticmethod
    def createMetas(metas):
        for meta in metas:
            db.session.add(meta)
        try:
            csvIds = []
            db.session.commit()
            for meta in metas:
                csvIds.append(meta.id)
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.remove()
            raise BaseException(e.__str__())

        return csvIds

    @staticmethod
    def getMetas():
        try:
            result = BiodiCsv.query.with_entities(BiodiCsv.id, BiodiCsv.fileName, BiodiCsv.createdBy, BiodiCsv.createdOn).all()
        except SQLAlchemyError as e:
            raise BaseException(e.__str__())

        return result