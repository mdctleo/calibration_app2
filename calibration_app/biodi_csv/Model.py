from app import db
from calibration_app.constants.Constants import *
from sqlalchemy.exc import *
from exceptions.Exceptions import *
import datetime

class Protocol(db.Model):
    __tablename__ = PROTOCOL_T_NAME
    id = db.Column(PROTOCOL_C_ID, db.Integer, primary_key=True, autoincrement=True)
    protocolName = db.Column(PROTOCOL_C_NAME, db.String(8), nullable=False)
    studyInformation = db.relationship('StudyInformation', backref=PROTOCOL_T_NAME)

    def __init__(self, protocolName):
        self.protocolName = protocolName

    def __repr__(self):
        return '<Protocol %r %r>' % (self.id, self.protocolName)


class Chelator(db.Model):
    __tablename__ = CHELATOR_T_NAME
    name = db.Column(CHELATOR_C_NAME, db.String(45), primary_key=True)
    studyInformation = db.relationship('StudyInformation', backref=CHELATOR_T_NAME)

class Vector(db.Model):
    __tablename__ = VECTOR_T_NAME
    name = db.Column(VECTOR_C_NAME, db.String(45), primary_key=True)
    type = db.Column(VECTOR_C_TYPE, db.String(45))
    studyInformation = db.relationship('StudyInformation', backref=VECTOR_T_NAME)

    def __repr__(self):
        return '<Vector %r %r>' % (self.name, self.type)

class TumorModel(db.Model):
    __tablename__ = TUMOR_MODEL_T_NAME
    name = db.Column(TUMOR_MODEL_C_NAME, db.String(45), primary_key=True)
    studyInformation = db.relationship('StudyInformation', backref=TUMOR_MODEL_T_NAME)

class MouseStrain(db.Model):
    __tablename__ = MOUSE_STRAIN_T_NAME
    name = db.Column(MOUSE_STRAIN_C_NAME, db.String(45), primary_key=True)
    studyInformation = db.relationship('StudyInformation', backref=MOUSE_STRAIN_T_NAME)

class Organ(db.Model):
    __tablename__ = ORGAN_T_NAME
    name = db.Column(ORGAN_C_NAME, db.String(45), primary_key=True)
    mouseOrgan = db.relationship('MouseOrgan', backref=ORGAN_T_NAME)

class CellLine(db.Model):
    __tablename__ = CELL_LINE_T_NAME
    name = db.Column(CELL_LINE_C_NAME, db.String(45), primary_key=True)
    studyInformation = db.relationship('StudyInformation', backref=CELL_LINE_T_NAME)


class StudyInformation(db.Model):
    __tablename__ = STUDY_INFORMATION_T_NAME
    id = db.Column(STUDY_INFORMATION_C_ID, db.Integer, primary_key=True, autoincrement=True)
    studyName = db.Column(STUDY_INFORMATION_C_STUDY_NAME, db.String(45), nullable=False)
    studyDate = db.Column(STUDY_INFORMATION_C_STUDY_DATE, db.Date, nullable=False)
    researcherName = db.Column(STUDY_INFORMATION_C_RESEARCHER_NAME, db.String(45), nullable=False)
    piName = db.Column(STUDY_INFORMATION_C_PI_NAME, db.String(45), nullable= False)
    isotopeName = db.Column(STUDY_INFORMATION_C_ISOTOPE, db.String(8), db.ForeignKey(ISOTOPE_T_NAME + '.' + ISOTOPE_C_ISOTOPE_NAME), nullable=False)
    chelatorName = db.Column(STUDY_INFORMATION_C_CHELATOR, db.String(8), db.ForeignKey(CHELATOR_T_NAME + '.' + CHELATOR_C_NAME), nullable=False)
    vectorName = db.Column(STUDY_INFORMATION_C_VECTOR, db.String(45), db.ForeignKey(VECTOR_T_NAME + '.' + VECTOR_C_NAME), nullable=False)
    target = db.Column(STUDY_INFORMATION_C_TARGET, db.String(45), nullable=False)
    cellLineName = db.Column(STUDY_INFORMATION_C_CELL_LINE, db.String(45), db.ForeignKey(CELL_LINE_T_NAME + '.' + CELL_LINE_C_NAME), nullable=False)
    tumorModelName = db.Column(STUDY_INFORMATION_C_TUMOR_MODEL, db.String(45), db.ForeignKey(TUMOR_MODEL_T_NAME + '.' + TUMOR_MODEL_C_NAME), nullable=False)
    mouseStrainName = db.Column(STUDY_INFORMATION_C_MOUSE_STRAIN, db.String(8), db.ForeignKey(MOUSE_STRAIN_T_NAME + '.' + MOUSE_STRAIN_C_NAME), nullable=False)
    radioPurity = db.Column(STUDY_INFORMATION_C_RADIO_PURITY, db.Float, nullable=False)
    comments = db.Column(STUDY_INFORMATION_C_COMMENTS, db.Text)
    gammaCounter = db.Column(STUDY_INFORMATION_C_GAMMA_COUNTER, db.String(8), db.ForeignKey(GAMMA_COUNTERS_T_NAME + '.' + GAMMA_COUNTERS_C_MODEL), nullable=False)
    runDateTime = db.Column(STUDY_INFORMATION_C_RUN_DATE_TIME, db.DateTime, nullable=False)
    gammaRunComments = db.Column(STUDY_INFORMATION_C_GAMMA_RUN_COMMENTS, db.Text)
    protocolId = db.Column(STUDY_INFORMATION_C_PROTOCOL_ID, db.Integer, db.ForeignKey(PROTOCOL_T_NAME + '.' + PROTOCOL_C_ID), nullable=False)
    createdOn = db.Column(STUDY_INFORMATION_C_CREATED_ON, db.TIMESTAMP, default=datetime.datetime.utcnow)
    biodiCsvRows = db.relationship('BiodiCsvRow', cascade="all, delete-orphan", backref=db.backref(STUDY_INFORMATION_T_NAME, lazy='joined'), lazy=True)
    mice = db.relationship('Mouse', cascade="all, delete-orphan", backref=db.backref(STUDY_INFORMATION_T_NAME, lazy='joined'), lazy=True)
    windows = db.relationship('Window', cascade="all, delete-orphan", backref=db.backref(STUDY_INFORMATION_T_NAME, lazy='joined'), lazy=True)


class Mouse(db.Model):
    __tablename__ = MOUSE_INFORMATION_T_NAME
    id = db.Column(MOUSE_INFORMATION_C_ID, db.Integer, primary_key=True, autoincrement=True)
    csvId = db.Column(MOUSE_INFORMATION_C_CSV_ID, db.Integer, db.ForeignKey(STUDY_INFORMATION_T_NAME + '.' + STUDY_INFORMATION_C_ID), nullable=False)
    mouseId = db.Column(MOUSE_INFORMATION_C_MOUSE_ID, db.String(20), nullable=False)
    groupId = db.Column(MOUSE_INFORMATION_C_GROUP_ID, db.String(20), nullable=False)
    euthanizeDateTime = db.Column(MOUSE_INFORMATION_C_EUTHANASIA_DATETIME, db.DateTime, nullable=False)
    gender = db.Column(MOUSE_INFORMATION_C_GENDER, db.CHAR, nullable=False)
    cage = db.Column(MOUSE_INFORMATION_C_CAGE, db.String(8), nullable=False)
    age = db.Column(MOUSE_INFORMATION_C_AGE, db.SmallInteger, nullable=False)
    injectionDate = db.Column(MOUSE_INFORMATION_C_INJECTION_DATE, db.Date, nullable=False)
    preInjectionTime = db.Column(MOUSE_INFORMATION_C_PRE_INJECTION_TIME, db.Time, nullable=False)
    injectionTime = db.Column(MOUSE_INFORMATION_C_INJECTION_TIME, db.Time, nullable=False)
    postInjectionTime = db.Column(MOUSE_INFORMATION_C_POST_INJECTION_TIME, db.Time, nullable=False)
    preInjectionActivity = db.Column(MOUSE_INFORMATION_C_PRE_INJECTION_ACTIVITY, db.Float, nullable=False)
    postInjectionActivity = db.Column(MOUSE_INFORMATION_C_POST_INJECTION_ACTIVITY, db.Float, nullable=False)
    mouseOrgans = db.relationship('MouseOrgan', cascade="all, delete-orphan", backref=db.backref(MOUSE_INFORMATION_T_NAME, lazy='joined'), lazy=True)


class MouseOrgan(db.Model):
    __tablename__ = MOUSE_ORGAN_T_NAME
    id = db.Column(MOUSE_ORGAN_C_ID, db.Integer, primary_key=True, autoincrement=True)
    mouseId = db.Column(MOUSE_ORGAN_C_MOUSE_ID, db.Integer, db.ForeignKey(MOUSE_INFORMATION_T_NAME + '.' + MOUSE_INFORMATION_C_ID), nullable=False)
    organName = db.Column(MOUSE_ORGAN_C_ORGAN_NAME, db.String(45), db.ForeignKey(ORGAN_T_NAME + '.' + ORGAN_C_NAME), nullable=False)
    organMass = db.Column(MOUSE_ORGAN_C_ORGAN_MASS, db.Float, nullable=False)

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

    def __repr__(self):
        return '<BiodiCsvRow %r>' % \
               (self.rowNum)


class Window(db.Model):
    __tablename__ = WINDOWS_T_NAME
    id = db.Column(WINDOWS_C_ID, db.Integer, primary_key=True, autoincrement=True)
    csvId = db.Column(WINDOWS_C_CSV_ID, db.Integer, db.ForeignKey(STUDY_INFORMATION_T_NAME + '.' + STUDY_INFORMATION_C_ID), nullable=False)
    rowNum = db.Column(WINDOWS_C_ROW_NUM, db.Integer, nullable=False)
    isotopeName = db.Column(WINDOWS_C_ISOTOPE, db.ForeignKey(ISOTOPE_T_NAME + '.' + ISOTOPE_C_ISOTOPE_NAME), nullable=False)
    counts = db.Column(WINDOWS_C_COUNTS, db.Float, nullable=False)
    cpm = db.Column(WINDOWS_C_CPM, db.Float, nullable=False)
    error = db.Column(WINDOWS_C_ERROR, db.Float, nullable=False)
    info = db.Column(WINDOWS_C_INFO, db.CHAR(1))

    def __repr__(self):
        return '<Widnow %r %r %r %r>' % (self.id, self.csvId, self.rowNum, self.isotopeName)