import csv
from io import StringIO
from calibration_app.biodi_csv.Model import MouseOrgan, BiodiCsvRow, StudyInformation, Mouse, Window
from calibration_app.biodi_csv.DatabaseHelper import DatabaseHelper as db
from exceptions.Exceptions import *
from methods.decay import calculateDecay, calculateCalibratedMouseActivity
from datetime import datetime
import pandas as pd

def getMetas():
    try:
        metas = db.getBiodiCsvMetas()
    except BaseException as e:
        raise e

    return metas

def getBiodiCsvRaw(studyId):
    try:
        completeStudy, isotope, calibrationFactor = db.getCompleteStudy(studyId)
        windowsMap = createWindowsMap(completeStudy.windows)
        si = StringIO()
        fieldnames = [
            "Protocol ID", "Protocol name", "Measurement date & time", "Completion status", "Run ID",
            "Rack", "Det", "Pos", "Time", "Sample code"
        ]

        for i, key in enumerate(windowsMap.keys()):
            fieldnames.append(key + " Counts")
            fieldnames.append(key + " Error %")
            fieldnames.append(key + " CPM")
            fieldnames.append(key + " Info")

        cw = csv.DictWriter(si, fieldnames=fieldnames)
        cw.writeheader()
        currRow=0

        for i, row in enumerate(completeStudy.biodiCsvRows):
            row = {
                "Protocol ID": completeStudy.protocolId,
                "Protocol name": db.getProtocolName(completeStudy.protocolId),
                "Measurement date & time": row.measurementTime,
                "Completion status": row.completionStatus,
                "Run ID": row.runId,
                "Rack": row.rack,
                "Det": row.det,
                "Pos": row.pos,
                "Time": row.time,
                "Sample code": row.sampleCode
            }

            for i, key in enumerate(windowsMap.keys()):
                row[key + " Counts"] = windowsMap[key][currRow].counts
                row[key + " Error %"] = windowsMap[key][currRow].error
                row[key + " CPM"] = windowsMap[key][currRow].cpm
                row[key + " Info"] = windowsMap[key][currRow].info

            cw.writerow(row)

            currRow = currRow + 1

        file = si.getvalue()
        print(file)
    except BaseException as e:
        raise e

    return file, completeStudy.studyName

def createWindowsMap(windows):
    windowsMap = {}
    for window in windows:
        windowsMap.setdefault(window.isotopeName, [])
        windowsMap[window.isotopeName].append(window)

    return windowsMap

def getCompleteStudy(studyId):
    try:

        completeStudy, isotope, calibrationFactor = db.getCompleteStudy(studyId)
        windowsMap = createWindowsMap(completeStudy.windows)
        si = StringIO()

        fieldnames = [
            "Isotope", "Chelator", "Vector", "Target", "VectorType", "Tumor Model", "Mouse Strain", "Mouse Gender", "Cage", "Mouse ID", "Injection Date",
            "Pre-injection (MBq)", "Pre-injection Time", "Post-injection (MBq)", "Post-injection Time", "Injection Time", "Injected Activity (kBq)",
            "Injection Time", "Injected Activity (kBq)", "Organ", "OrganMass(g)", "Euthanasia Date", "Euthanasia Time", "TimePoint (h)",
            "Count#", "Rack", "Vial", "Time", "Counted Time (s)", "Dead Time Factor"]

        for i, key in enumerate(windowsMap.keys()):
            currWinNum = str((i + 1))
            fieldnames.append("Dead Time Factor" + currWinNum)
            fieldnames.append("IsotopeWin" + currWinNum)
            fieldnames.append("Window" + currWinNum + " (counts)")
            fieldnames.append("Window" + currWinNum + " corrected (counts)")
            fieldnames.append("Window" + currWinNum + " (CPM)")
            fieldnames.append("Normalized Window" + currWinNum + " (CPM)")
            fieldnames.append("Normalized Window" + currWinNum + " (Bq)")
            fieldnames.append("Window " + currWinNum + " %ID/g @ injectionTime")


        cw = csv.DictWriter(si, fieldnames=fieldnames)
        cw.writeheader()
        currRow = 0

        for i, mouse in enumerate(completeStudy.mice):
            for j, organ in enumerate(mouse.mouseOrgans):
                biodiCsvRow = completeStudy.biodiCsvRows[currRow]

                preInjectionTime = datetime.combine(mouse.injectionDate, mouse.preInjectionTime)
                postInjectionTime = datetime.combine(mouse.injectionDate, mouse.postInjectionTime)
                injectionTime = datetime.combine(mouse.injectionDate, mouse.injectionTime)
                preInjectedActivity = calculateDecay(mouse.preInjectionActivity, preInjectionTime, injectionTime, isotope.halfLife)
                postInjectedActivity = calculateDecay(mouse.postInjectionActivity, injectionTime, postInjectionTime, isotope.halfLife)
                injectedActivity = preInjectedActivity - postInjectedActivity


                row = {
                    'Isotope': completeStudy.isotopeName,
                    'Chelator': completeStudy.chelatorName,
                    'Vector': completeStudy.vectorName,
                    'Target': completeStudy.target,
                    'VectorType': db.getVector(completeStudy.vectorName).type,
                    'Tumor Model': completeStudy.tumorModelName,
                    'Mouse Strain': completeStudy.mouseStrainName,
                    'Mouse Gender': mouse.gender,
                    'Cage': mouse.cage,
                    'Mouse ID': mouse.mouseId,
                    'Injection Date': mouse.injectionDate,
                    'Pre-injection (MBq)': mouse.preInjectionActivity,
                    'Pre-injection Time': mouse.preInjectionTime,
                    'Post-injection (MBq)': mouse.postInjectionActivity,
                    'Post-injection Time': mouse.postInjectionTime,
                    'Injection Time': mouse.injectionTime,
                    'Injected Activity (kBq)': injectedActivity,
                    'Organ': organ.organName,
                    'OrganMass(g)': organ.organMass,
                    'Euthanasia Date': mouse.euthanizeDateTime.date(),
                    'Euthanasia Time': mouse.euthanizeDateTime.time(),
                    'TimePoint (h)': mouse.groupId,
                    'Count#': biodiCsvRow.det,
                    'Rack': biodiCsvRow.rack,
                    'Vial': j,
                    'Time': biodiCsvRow.measurementTime,
                    'Counted Time (s)': biodiCsvRow.time,
                }

                for k, key in enumerate(windowsMap.keys()):
                    mouseAcitivty = calculateCalibratedMouseActivity(windowsMap[key][currRow].cpm, isotope.halfLife,
                                                                     injectionTime, biodiCsvRow.measurementTime, calibrationFactor)

                    currWinNum = str((k + 1))
                    cpm = windowsMap[key][currRow].cpm
                    row['Dead Time Factor' + currWinNum] = "PlaceHolder"
                    row["IsotopeWin" + currWinNum] = key
                    row["Window" + currWinNum + " (counts)"] = windowsMap[key][currRow].counts
                    row["Window" + currWinNum + " corrected (counts)"] = windowsMap[key][currRow].counts
                    row["Window" + currWinNum + " (CPM)"] = cpm
                    row["Normalized Window" + currWinNum + " (CPM)"] =  windowsMap[key][currRow].cpm
                    row["Normalized Window" + currWinNum + " (Bq)" ] = "PlaceHolder"
                    row["Window " + currWinNum + " %ID/g @ injectionTime"] = ((mouseAcitivty / injectedActivity) * 100) / organ.organMass





                cw.writerow(row)

                currRow = currRow + 1

        file = si.getvalue()

    except BaseException as e:
        raise e

    return file, completeStudy.studyName

def getStudyAnalysis(studyId):
    completeStudy, isotope, calibrationFactor = db.getCompleteStudy(studyId)
    pd.read_sql(db.getCompleteStudy(studyId))
    return None

def getChelators():
    try:
        result = db.getChelators()
    except BaseException as e:
        raise e

    return result

def getVectors():
    try:
        result = db.getVectors()
    except BaseException as e:
        raise e

    return result

def getCellLines():
    try:
        result = db.getCellLines()
    except BaseException as e:
        raise e

    return result

def getMouseStrains():
    try:
        result = db.getMouseStrains()
    except BaseException as e:
        raise e

    return result

def getTumorModels():
    try:
        result = db.getTumorModels()
    except BaseException as e:
        raise e

    return result
