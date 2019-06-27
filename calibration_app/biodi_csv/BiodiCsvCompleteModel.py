from app import db
from calibration_app.constants.Constants import *
from sqlalchemy.exc import *
from exceptions.Exceptions import *
import datetime


class Chelator(db.Model):
    __tablename__ = CHELATOR_T_NAME
    name = db.Column(CHELATOR_C_NAME, db.String(45), primary_key=True)


class Vector(db.Model):
    __tablename__ = VECTOR_T_NAME
    name = db.Column(VECTOR_C_NAME, db.String(45), primary_key=True)
    type = db.Column(VECTOR_C_TYPE, db.String(45))


class TumorModel(db.Model):
    __tablename__ = TUMOR_MODEL_T_NAME
    model = db.Column(TUMOR_MODEL_C_MODEL, db.String(45), primary_key=True)


class MouseStrain(db.Model):
    __tablename__ = MOUSE_STRAIN_T_NAME
    strain = db.Column(MOUSE_STRAIN_C_STRAIN, db.String(45), primary_key=True)


class Organ(db.Model):
    __tablename__ = BIODI_CSV_COMPLETE_VALUES_C_ORGAN
    name = db.Column(BIODI_CSV_COMPLETE_VALUES_C_ORGAN, db.String(45), primary_key=True)


class BiodiCsvComplete(db.Model):
    __tablename__ = BIODI_CSV_COMPLETE_T_NAME
    id = db.Column(BIODI_CSV_COMPLETE_VALUES_C_ID, db.Integer, primary_key=True, autoincrement=True)
    studyName = db.Column(BIODICSV_COMPLETE_VALUES_C_STUD)
    fileName = db.Column(BIODI_CSV_COMPLETE_C_FILE_NAME, db.String(45), nullable=False)
    isotope = db.Column(BIODI_CSV_COMPLETE_C_ISOTOPE, db.String(8), nullable=False)
    chelator = db.Column(BIODI_CSV_COMPLETE_C_CHELATOR, db.String(8), nullable=False)
    vector = db.Column(BIODI_CSV_COMPLETE_C_VECTOR, db.String(45), nullable=False)
    tumorModel = db.Column(BIODI_CSV_COMPLETE_C_TUMOR_MODEL, db.String(45), nullable=False)
    mouseStrain = db.Column(BIODI_CSV_COMPLETE_C_MOUSE_STRAIN, db.String(8), nullable=False)

    def __init__(self, fileName, isotope, chelator, vector, tumorModel, mouseStrain):
        self.fileName = fileName
        self.isotope = isotope
        self.chelator = chelator
        self.vector = vector
        self.tumorModel = tumorModel
        self.mouseStrain = mouseStrain


class BiodiCsvCompleteRows(db.Model):
    __tablename__ = BIODI_CSV_COMPLETE_VALUES_T_NAME
    id = db.Column(BIODI_CSV_COMPLETE_VALUES_C_ID, db.Integer, primary_key=True, autoincrement=True)
    rowNumber = db.Column(BIODI_CSV_COMPLETE_VALUES_C_ROW_NUMBER, db.Integer, nullable=False)
    csvId = db.Column(BIODI_CSV_COMPLETE_VALUES_C_CSV_ID, db.Integer, nullable=False)
    mouseGender = db.Column(BIODI_CSV_COMPLETE_VALUES_C_MOUSE_GENDER, db.CHAR, nullable=False)
    cage = db.Column(BIODI_CSV_COMPLETE_VALUES_C_CAGE, db.String(8), nullable=False)
    mouseId = db.Column(BIODI_CSV_COMPLETE_VALUES_C_MOUSE_ID, db.String(20), nullable=False)
    injectionDate = db.Column(BIODI_CSV_COMPLETE_VALUES_C_INJECTION_DATE, db.Date, nullable=False)
    preInjectionTime = db.Column(BIODI_CSV_COMPLETE_VALUES_C_PRE_INJECTION_TIME, db.Time, nullable=False)
    injectionTime = db.Column(BIODI_CSV_COMPLETE_VALUES_C_INJECTION_TIME, db.Time, nullable=False)
    postInjectionTime = db.Column(BIODI_CSV_COMPLETE_VALUES_C_POST_INJECTION_TIME, db.Time, nullable=False)
    preInjectionActivity = db.Column(BIODI_CSV_COMPLETE_VALUES_C_PRE_INJECTION_ACTIVITY, db.Float, nullable=False)
    postInjectionActivity = db.Column(BIODI_CSV_COMPLETE_VALUES_C_POST_INJECTION_ACTIVITY, db.Float, nullable=False)
    organ = db.Column(BIODI_CSV_COMPLETE_VALUES_C_ORGAN, db.String(45), nullable=False)
    organMass = db.Column(BIODI_CSV_COMPLETE_VALUES_C_ORGAN_MASS, db.Float, nullable=False)
    euthanizeDateTime = db.Column(BIODI_CSV_COMPLETE_VALUES_C_EUTHANIZE_DATETIME, db.DateTime, nullable=False)
    timepoint = db.Column(BIODI_CSV_COMPLETE_VALUES_C_TIMEPOINT, db.SmallInteger, nullable=False)
    count = db.Column(BIODI_CSV_COMPLETE_VALUES_C_COUNT, db.Integer, nullable=False)
    rack = db.Column(BIODI_CSV_COMPLETE_VALUES_C_RACK, db.SmallInteger, nullable=False)
    vial = db.Column(BIODI_CSV_COMPLETE_VALUES_C_VIAL, db.SmallInteger, nullable=False)
    time = db.Column(BIODI_CSV_COMPLETE_VALUES_C_TIME, db.DateTime, nullable=False)
    deadTimeFactor = db.Column(BIODI_CSV_COMPLETE_VALUES_C_DEAD_TIME_FACTOR, db.Float, nullable=False)


class Windows(db.Model):
    __tablenme__ = WINDOWS_T_NAME
    id = db.Column(WINDOWS_C_ID, db.Integer, primary_key=True, autoincrement=True)
    rowNumber = db.Column(WINDOWS_C_ROW_NUM, db.Integer, nullable=False)
    csvId = db.Column(WINDOWS_C_CSV_ID, db.Integer, nullable=False)
    windowNum = db.Column(WINDOWS_C_WINDOW_NUM, db.SmallInteger, nullable=False)
    isotope = db.Column(WINDOWS_C_ISOTOPE, db.String(8), nullable=False)
    counts = db.Column(WINDOWS_C_COUNTS, db.Integer, nullable=False)
    correctedCounts = db.Column(WINDOWS_C_CORRECTED_COUNTS, db.Integer, nullable=False)
    cpm = db.Column(WINDOWS_C_CPM, db.Integer, nullable=False)
