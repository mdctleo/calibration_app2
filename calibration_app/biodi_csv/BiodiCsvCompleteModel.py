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
    name = db.Column(TUMOR_MODEL_C_NAME, db.String(45), primary_key=True)
    studyInformation = db.relationship('StudyInformation', backref=TUMOR_MODEL_T_NAME)

    def __init__(self, name):
        self.name = name


class MouseStrain(db.Model):
    __tablename__ = MOUSE_STRAIN_T_NAME
    name = db.Column(MOUSE_STRAIN_C_NAME, db.String(45), primary_key=True)
    studyInformation = db.relationship('StudyInformation', backref=MOUSE_STRAIN_T_NAME)

    def __init__(self, name):
        self.name = name

class Organ(db.Model):
    __tablename__ = ORGAN_T_NAME
    name = db.Column(ORGAN_C_NAME, db.String(45), primary_key=True)
    studyInformation = db.relationship('BiodiCsvCompleteRow', backref=ORGAN_T_NAME)

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
    gammaRunCommnets = db.Column(STUDY_INFORMATION_C_GAMMA_RUN_COMMENTS, db.Text)
    protocolId = db.Column(STUDY_INFORMATION_C_PROTOCOL_ID, db.Integer, db.ForeignKey(PROTOCOL_T_NAME + '.' + PROTOCOL_C_ID), nullable=False)
    biodiCsvRow = db.relationship('BiodiCsvRow', cascade="all, delete-orphan", backref=STUDY_INFORMATION_T_NAME)
    biodiCsvCompleteRow = db.relationship('BiodiCsvCompleteRow', cascade="all, delete-orphan", backref=STUDY_INFORMATION_T_NAME)
    # windows = db.relationship('Window', cascade="all, delete-orphan", backref=STUDY_INFORMATION_T_NAME)
    mouse = db.relationship('Mouse', cascade="all, delete-orphan", backref=STUDY_INFORMATION_T_NAME)

    def __init__(self, studyName, studyDate, researcherName, piName, isotopeName, chelatorName, vectorName, target, cellLineName, tumorModelName,
                 mouseStrainName, radioPurity, comments, gammaCounter, runDateTime, gammaRunComments, protocolId,
                 biodiCsvRows, biodiCsvCompleteRows, mice):
        self.studyName = studyName
        self.studyDate = studyDate
        self.researcherName = researcherName
        self.piName = piName
        self.isotopeName = isotopeName
        self.chelatorName = chelatorName
        self.vectorName = vectorName
        self.target = target
        self.cellLineName = cellLineName
        self.tumorModelName = tumorModelName
        self.mouseStrainName = mouseStrainName
        self.radioPurity = radioPurity
        self.comments = comments
        self.gammaCounter = gammaCounter
        self.runDateTime = runDateTime
        self.gammaRunCommnets = gammaRunComments
        self.protocolId = protocolId
        self.biodiCsvRow = biodiCsvRows
        self.biodiCsvCompleteRow = biodiCsvCompleteRows
        self.mouse = mice

class Mouse(db.Model):
    __tablename__ = MOUSE_INFORMATION_T_NAME
    id = db.Column(MOUSE_INFORMATION_C_ID, db.Integer, primary_key=True, autoincrement=True)
    csvId = db.Column(MOUSE_INFORMATION_C_CSV_ID, db.Integer, db.ForeignKey(STUDY_INFORMATION_T_NAME + '.' + STUDY_INFORMATION_C_ID), nullable=False)
    mouseId = db.Column(MOUSE_INFORMATION_C_MOUSE_ID, db.String(20), nullable=False)
    groupId = db.Column(MOUSE_INFORMATION_C_GROUP_ID, db.String(20), nullable=False)
    euthanizeDateTime = db.Column(MOUSE_INFORMATION_C_EUTHANASIA_DATETIME, db.DateTime, nullable=False)
    mouseGender = db.Column(MOUSE_INFORMATION_C_GENDER, db.CHAR, nullable=False)
    cage = db.Column(MOUSE_INFORMATION_C_CAGE, db.String(8), nullable=False)
    age = db.Column(MOUSE_INFORMATION_C_AGE, db.SmallInteger, nullable=False)
    injectionDate = db.Column(MOUSE_INFORMATION_C_INJECTION_DATE, db.Date, nullable=False)
    preInjectionTime = db.Column(MOUSE_INFORMATION_C_PRE_INJECTION_TIME, db.Time, nullable=False)
    injectionTime = db.Column(MOUSE_INFORMATION_C_INJECTION_TIME, db.Time, nullable=False)
    postInjectionTime = db.Column(MOUSE_INFORMATION_C_POST_INJECTION_TIME, db.Time, nullable=False)
    preInjectionActivity = db.Column(MOUSE_INFORMATION_C_PRE_INJECTION_ACTIVITY, db.Float, nullable=False)
    postInjectionActivity = db.Column(MOUSE_INFORMATION_C_POST_INJECTION_ACTIVITY, db.Float, nullable=False)

    def __init__(self, mouseId, groupId, euthanizeDateTime, mouseGender, cage, age, injectionDate, preInjectionTime,
                 injectionTime, postInjectionTime, preInjectionActivity, postInjectionActivity):
        self.mouseId = mouseId
        self.groupId = groupId
        self.euthanizeDateTime = euthanizeDateTime
        self.mouseGender = mouseGender
        self.cage = cage
        self.age = age
        self.injectionDate = injectionDate
        self.preInjectionTime = preInjectionTime
        self.injectionTime = injectionTime
        self.postInjectionTime = postInjectionTime
        self.preInjectionActivity = preInjectionActivity
        self.postInjectionActivity = postInjectionActivity




class BiodiCsvCompleteRow(db.Model):
    __tablename__ = BIODI_CSV_COMPLETE_ROWS_T_NAME
    id = db.Column(BIODI_CSV_COMPLETE_ROWS_C_ID, db.Integer, primary_key=True, autoincrement=True)
    rowNumber = db.Column(BIODI_CSV_COMPLETE_ROWS_C_ROW_NUMBER, db.Integer, nullable=False)
    csvId = db.Column(BIODI_CSV_COMPLETE_ROWS_C_CSV_ID, db.Integer, db.ForeignKey(STUDY_INFORMATION_T_NAME + '.' + STUDY_INFORMATION_C_ID), nullable=False)
    organName = db.Column(BIODI_CSV_COMPLETE_ROWS_C_ORGAN, db.String(45), db.ForeignKey(ORGAN_T_NAME + '.' + ORGAN_C_NAME), nullable=False)
    organMass = db.Column(BIODI_CSV_COMPLETE_ROWS_C_ORGAN_MASS, db.Float, nullable=False)
    # count = db.Column(BIODI_CSV_COMPLETE_ROWS_C_COUNT, db.Integer, nullable=False)
    # rack = db.Column(BIODI_CSV_COMPLETE_ROWS_C_RACK, db.SmallInteger, nullable=False)
    # vial = db.Column(BIODI_CSV_COMPLETE_ROWS_C_VIAL, db.SmallInteger, nullable=False)
    deadTimeFactor = db.Column(BIODI_CSV_COMPLETE_ROWS_C_DEAD_TIME_FACTOR, db.Float, nullable=False)

    # TODO: this is a lot of parameters, perhaps pass in a dictionary instead?
    def __init__(self, rowNumber, organ, organMass, deadTimeFactor):
        self.rowNumber = rowNumber
        self.organ = organ
        self.organMass = organMass
        # self.count = count
        # self.rack = rack
        # self.vial = vial
        self.deadTimeFactor = deadTimeFactor



# class Window(db.Model):
#     __tablenme__ = WINDOWS_T_NAME
#     id = db.Column(WINDOWS_C_ID, db.Integer, primary_key=True, autoincrement=True)
#     rowNumber = db.Column(WINDOWS_C_ROW_NUM, db.Integer, nullable=False)
#     csvId = db.Column(WINDOWS_C_CSV_ID, db.Integer, db.ForeignKey(STUDY_INFORMATION_T_NAME + '.' + STUDY_INFORMATION_C_ID), nullable=False)
#     windowNum = db.Column(WINDOWS_C_WINDOW_NUM, db.SmallInteger, nullable=False)
#     # counts = db.Column(WINDOWS_C_COUNTS, db.Integer, nullable=False)
#     # correctedCounts = db.Column(WINDOWS_C_CORRECTED_COUNTS, db.Integer, nullable=False)
#     # cpm = db.Column(WINDOWS_C_CPM, db.Integer, nullable=False)
#
#     def __init__(self, rowNumber, windowNum, isotope):
#         self.rowNumber = rowNumber
#         self.windowNum = windowNum
#         self.isotope = isotope
#         # self.counts = counts
#         # self.correctedCounts = correctedCounts
#         # self.cpm = cpm
