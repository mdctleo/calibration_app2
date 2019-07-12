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
    studyInformation = db.relationship('StudyInformation', backref=PROTOCOL_T_NAME)

    def __init__(self, protocolName):
        self.protocolName = protocolName

    def __repr__(self):
        return '<Protocol %r %r>' % (self.id, self.protocolName)


# class BiodiCsv(db.Model):
#     __tablename__ = BIODI_CSV_T_NAME
#     id = db.Column(BIODI_CSV_C_ID, db.Integer, primary_key=True, autoincrement=True)
#     fileName = db.Column(BIODI_CSV_C_FILE_NAME, db.String(45), nullable=False)
#     protocolId = db.Column(BIODI_CSV_C_PROTOCOL_ID, db.Integer, db.ForeignKey(PROTOCOL_T_NAME + '.' + PROTOCOL_C_ID), nullable=False)
#     createdOn = db.Column(BIODI_CSV_C_CREATED_ON, db.TIMESTAMP, default=datetime.datetime.utcnow)
#     createdBy = db.Column(BIODI_CSV_C_CREATED_BY, db.String(100), nullable=False)
#     biodiCsvValues = db.relationship('BiodiCsvRow', cascade="all, delete-orphan", backref=BIODI_CSV_T_NAME)
#
#     def __init__(self, fileName, protocolId, createdBy):
#         self.fileName = fileName
#         self.protocolId = protocolId
#         self.createdBy = createdBy
#
#     def __repr__(self):
#         return '<BiodiCsv %r %r %r>' % (self.id, self.fileName, self.protocolId)
#
#     @property
#     def fileName(self):
#         return self.fileName


class BiodiCsvRow(db.Model):
    __tablename__ = BIODI_CSV_ROWS_T_NAME
    id = db.Column(BIODI_CSV_ROWS_C_ID, db.Integer, primary_key=True, autoincrement=True)
    csvId = db.Column(BIODI_CSV_ROWS_C_CSV_ID, db.Integer, db.ForeignKey(STUDY_INFORMATION_T_NAME + '.' + STUDY_INFORMATION_C_ID), nullable=False)
    rowNum = db.Column(BIODI_CSV_ROWS_C_ROW_NUM, db.Integer, nullable=False)
    measurementTime = db.Column(BIODI_CSV_ROWS_C_MEASUREMENT_DATETIME, db.DateTime)
    completionStatus = db.Column(BIODI_CSV_ROWS_C_COMPLETION_STATUS, db.Integer)
    runId = db.Column(BIODI_CSV_ROWS_C_RUN_ID, db.Integer)
    rack = db.Column(BIODI_CSV_ROWS_C_RACK, db.Integer)
    det = db.Column(BIODI_CSV_ROWS_C_DET, db.Integer)
    pos = db.Column(BIODI_CSV_ROWS_C_POS, db.Integer)
    time = db.Column(BIODI_CSV_ROWS_C_TIME, db.Float)
    sampleCode = db.Column(BIODI_CSV_ROWS_C_SAMPLE_CODE, db.String(45))
    counts = db.Column(BIODI_CSV_ROWS_C_COUNTS, db.Float)
    cpm = db.Column(BIODI_CSV_ROWS_C_CPM, db.Float)
    error = db.Column(BIODI_CSV_ROWS_C_ERROR, db.Float)
    info = db.Column(BIODI_CSV_ROWS_C_INFO, db.CHAR(1))

    # def __repr__(self):
    #     return '<BiodiCsvRow %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r>' % \
    #            (self.id, self.csvId, self.rowNum, self.measurementTime, self.completionStatus,
    #             self.runId, self.rack, self.det, self.pos, self.time, self.sampleCode, self.counts,
    #             self.cpm, self.error, self.info)

    def __repr__(self):
        return '<BiodiCsvRow %r>' % \
               (self.rowNum)