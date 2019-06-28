from app import db
from calibration_app.constants.Constants import *
from sqlalchemy.exc import *
from exceptions.Exceptions import *
import datetime


class Chelator(db.Model):
    __tablename__ = CHELATOR_T_NAME
    name = db.Column(CHELATOR_C_NAME, db.String(45), primary_key=True)
    studyInformation = db.relationship('StudyInformation', backref=CHELATOR_T_NAME)

    def __init__(self, name):
        self.name = name


class Vector(db.Model):
    __tablename__ = VECTOR_T_NAME
    name = db.Column(VECTOR_C_NAME, db.String(45), primary_key=True)
    type = db.Column(VECTOR_C_TYPE, db.String(45))
    studyInformation = db.relationship('StudyInformation', backref=VECTOR_T_NAME)

    def __init__(self, name, type):
        self.name = name
        self.type = type


class TumorModel(db.Model):
    __tablename__ = TUMOR_MODEL_T_NAME
    model = db.Column(TUMOR_MODEL_C_MODEL, db.String(45), primary_key=True)
    studyInformation = db.relationship('StudyInformation', backref=TUMOR_MODEL_T_NAME)

    def __init__(self, model):
        self.model = model


class MouseStrain(db.Model):
    __tablename__ = MOUSE_STRAIN_T_NAME
    strain = db.Column(MOUSE_STRAIN_C_STRAIN, db.String(45), primary_key=True)
    studyInformation = db.relationship('StudyInformation', backref=MOUSE_STRAIN_T_NAME)

    def __init__(self, strain):
        self.strain = strain


class Organ(db.Model):
    __tablename__ = ORGAN_T_NAME
    name = db.Column(ORGAN_C_NAME, db.String(45), primary_key=True)
    studyInformation = db.relationship('BiodiCsvCompleteRows', backref=ORGAN_T_NAME)

    def __init__(self, name):
        self.name = name

class CellLine(db.Model):
    __tablename__ = CELL_LINE_T_NAME
    name = db.Column(CELL_LINE_C_NAME, db.String(45), primary_key=True)
    studyInformation = db.relationship('StudyInformation', backref=CELL_LINE_T_NAME)

    def __init__(self, name):
        self.name = name


class StudyInformation(db.Model):
    __tablename__ = STUDY_INFORMATION_T_NAME
    id = db.Column(STUDY_INFORMATION_C_ID, db.Integer, primary_key=True, autoincrement=True)
    studyName = db.Column(STUDY_INFORMATION_C_STUDY_NAME, db.String(45), nullable=False)
    isotope = db.Column(STUDY_INFORMATION_C_ISOTOPE, db.String(8), db.ForeignKey(ISOTOPE_T_NAME + '.' + ISOTOPE_C_ISOTOPE_NAME), nullable=False)
    chelator = db.Column(STUDY_INFORMATION_C_CHELATOR, db.String(8), db.ForeignKey(CHELATOR_T_NAME + '.' + CHELATOR_C_NAME), nullable=False)
    vector = db.Column(STUDY_INFORMATION_C_VECTOR, db.String(45), db.ForeignKey(VECTOR_T_NAME + '.' + VECTOR_C_NAME), nullable=False)
    cellLine = db.Column(STUDY_INFORMATION_C_CELL_LINE, db.String(45), db.ForeignKey(CELL_LINE_T_NAME + '.' + CELL_LINE_C_NAME), nullable=False)
    tumorModel = db.Column(STUDY_INFORMATION_C_TUMOR_MODEL, db.String(45), db.ForeignKey(TUMOR_MODEL_T_NAME + '.' + TUMOR_MODEL_C_MODEL), nullable=False)
    mouseStrain = db.Column(STUDY_INFORMATION_C_MOUSE_STRAIN, db.String(8), db.ForeignKey(MOUSE_STRAIN_T_NAME + '.' + MOUSE_STRAIN_C_STRAIN), nullable=False)
    radioActivity = db.Column(STUDY_INFORMATION_C_RADIO_ACTIVITY, db.Float, nullable=False)
    radioPurity = db.Column(STUDY_INFORMATION_C_RADIO_PURITY, db.Float, nullable=False)
    comments = db.Column(STUDY_INFORMATION_C_COMMENTS, db.Text)
    gammaCounter = db.Column(STUDY_INFORMATION_C_GAMMA_COUNTER, db.String(8), db.ForeignKey(GAMMA_COUNTERS_T_NAME + '.' + GAMMA_COUNTERS_C_MODEL), nullable=False)
    runDateTime = db.Column(STUDY_INFORMATION_C_RUN_DATE_TIME, db.DateTime, nullable=False)
    gammaRunCommnets = db.Column(STUDY_INFORMATION_C_GAMMA_RUN_COMMENTS, db.Text)
    protocolId = db.Column(STUDY_INFORMATION_C_PROTOCOL_ID, db.Integer, db.ForeignKey(PROTOCOL_T_NAME + '.' + PROTOCOL_C_NAME), nullable=False)
    biodiCsvRows = db.relationship('BiodiCsvRows', cascade="all, delete-orphan", backref=STUDY_INFORMATION_T_NAME)
    biodiCsvCompleteRows = db.relationship('BiodiCsvCompleteRows', cascade="all, delete-orphan", backref=STUDY_INFORMATION_T_NAME)
    windows = db.relationship('Windows', cascade="all, delete-orphan", backref=STUDY_INFORMATION_T_NAME)

    def __init__(self, fileName, isotope, chelator, vector, tumorModel, mouseStrain):
        self.fileName = fileName
        self.isotope = isotope
        self.chelator = chelator
        self.vector = vector
        self.tumorModel = tumorModel
        self.mouseStrain = mouseStrain


class BiodiCsvCompleteRow(db.Model):
    __tablename__ = BIODI_CSV_COMPLETE_ROWS_T_NAME
    id = db.Column(BIODI_CSV_COMPLETE_ROWS_C_ID, db.Integer, primary_key=True, autoincrement=True)
    rowNumber = db.Column(BIODI_CSV_COMPLETE_ROWS_C_ROW_NUMBER, db.Integer, nullable=False)
    csvId = db.Column(BIODI_CSV_COMPLETE_ROWS_C_CSV_ID, db.Integer, db.ForeignKey(STUDY_INFORMATION_T_NAME + '.' + STUDY_INFORMATION_C_ID), nullable=False)
    mouseGender = db.Column(BIODI_CSV_COMPLETE_ROWS_C_MOUSE_GENDER, db.CHAR, nullable=False)
    cage = db.Column(BIODI_CSV_COMPLETE_ROWS_C_CAGE, db.String(8), nullable=False)
    mouseId = db.Column(BIODI_CSV_COMPLETE_ROWS_C_MOUSE_ID, db.String(20), nullable=False)
    injectionDate = db.Column(BIODI_CSV_COMPLETE_ROWS_C_INJECTION_DATE, db.Date, nullable=False)
    preInjectionTime = db.Column(BIODI_CSV_COMPLETE_ROWS_C_PRE_INJECTION_TIME, db.Time, nullable=False)
    injectionTime = db.Column(BIODI_CSV_COMPLETE_ROWS_C_INJECTION_TIME, db.Time, nullable=False)
    postInjectionTime = db.Column(BIODI_CSV_COMPLETE_ROWS_C_POST_INJECTION_TIME, db.Time, nullable=False)
    preInjectionActivity = db.Column(BIODI_CSV_COMPLETE_ROWS_C_PRE_INJECTION_ACTIVITY, db.Float, nullable=False)
    postInjectionActivity = db.Column(BIODI_CSV_COMPLETE_ROWS_C_POST_INJECTION_ACTIVITY, db.Float, nullable=False)
    organ = db.Column(BIODI_CSV_COMPLETE_ROWS_C_ORGAN, db.String(45), db.ForeignKey(ORGAN_T_NAME + '.' +  ORGAN_C_NAME), nullable=False)
    organMass = db.Column(BIODI_CSV_COMPLETE_ROWS_C_ORGAN_MASS, db.Float, nullable=False)
    euthanizeDateTime = db.Column(BIODI_CSV_COMPLETE_ROWS_C_EUTHANIZE_DATETIME, db.DateTime, nullable=False)
    timepoint = db.Column(BIODI_CSV_COMPLETE_ROWS_C_TIMEPOINT, db.SmallInteger, nullable=False)
    count = db.Column(BIODI_CSV_COMPLETE_ROWS_C_COUNT, db.Integer, nullable=False)
    rack = db.Column(BIODI_CSV_COMPLETE_ROWS_C_RACK, db.SmallInteger, nullable=False)
    vial = db.Column(BIODI_CSV_COMPLETE_ROWS_C_VIAL, db.SmallInteger, nullable=False)
    time = db.Column(BIODI_CSV_COMPLETE_ROWS_C_TIME, db.DateTime, nullable=False)
    deadTimeFactor = db.Column(BIODI_CSV_COMPLETE_ROWS_C_DEAD_TIME_FACTOR, db.Float, nullable=False)

    # TODO: this is a lot of parameters, perhaps pass in a dictionary instead?
    def __init__(self, rowNumber, csvId, mouseGender, cage, mouseId, injectionDate, preInjectionTime, postInjectionTime,
                 preInjectionActivity, postInjectionActivity, organ, organMass, euthanizeDateTime, timepoint, count,
                 rack, vial, time, deadTimeFactor):
        self.rowNumber = rowNumber
        self.csvId = csvId
        self.mouseGender = mouseGender
        self.cage = cage
        self.mouseId = mouseId
        self.injectionDate = injectionDate
        self.preInjectionTime = preInjectionTime
        self.postInjectionTime = postInjectionTime
        self.preInjectionActivity = preInjectionActivity
        self.postInjectionActivity = postInjectionActivity
        self.organ = organ
        self.organMass = organMass
        self.euthanizeDateTime = euthanizeDateTime
        self.timepoint = timepoint
        self.count = count
        self.rack = rack
        self.vial = vial
        self.time = time
        self.deadTimeFactor = deadTimeFactor



class Windows(db.Model):
    __tablenme__ = WINDOWS_T_NAME
    id = db.Column(WINDOWS_C_ID, db.Integer, primary_key=True, autoincrement=True)
    rowNumber = db.Column(WINDOWS_C_ROW_NUM, db.Integer, nullable=False)
    csvId = db.Column(WINDOWS_C_CSV_ID, db.Integer, db.ForeignKey(STUDY_INFORMATION_T_NAME + '.' + STUDY_INFORMATION_C_ID), nullable=False)
    windowNum = db.Column(WINDOWS_C_WINDOW_NUM, db.SmallInteger, nullable=False)
    isotope = db.Column(WINDOWS_C_ISOTOPE, db.String(8), nullable=False)
    counts = db.Column(WINDOWS_C_COUNTS, db.Integer, nullable=False)
    correctedCounts = db.Column(WINDOWS_C_CORRECTED_COUNTS, db.Integer, nullable=False)
    cpm = db.Column(WINDOWS_C_CPM, db.Integer, nullable=False)

    def __init__(self, rowNumber, csvId, windowNum, isotope, counts, correctedCounts, cpm):
        self.rowNumber = rowNumber
        self.csvId = csvId
        self.windowNum = windowNum
        self.isotope = isotope
        self.counts = counts
        self.correctedCounts = correctedCounts
        self.cpm = cpm
