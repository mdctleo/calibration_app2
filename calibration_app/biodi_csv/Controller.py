import csv
from io import StringIO
from calibration_app.biodi_csv.Model import MouseOrgan, BiodiCsvRow, StudyInformation, Mouse, Window
from calibration_app.biodi_csv.DatabaseHelper import DatabaseHelper as db
from exceptions.Exceptions import *
import datetime

def getMetas():
    try:
        metas = db.getBiodiCsvMetas()
    except BaseException as e:
        raise e

    return metas

def getBiodiCsvRaw(studyId):
    try:
        completeStudy, windows = db.getCompleteStudy(studyId)
        windowsMap = createWindowsMap(windows)
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

        completeStudy, windows = db.getCompleteStudy(studyId)
        windowsMap = createWindowsMap(windows)
        si = StringIO()

        fieldnames = [
            "Isotope", "Chelator", "Vector", "VectorType", "Tumor Model", "Mouse Strain", "Mouse Gender", "Cage", "Mouse ID", "Injection Date",
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


        cw = csv.DictWriter(si, fieldnames=fieldnames)
        cw.writeheader()
        currRow = 0

        for i, mouse in enumerate(completeStudy.mice):
            for j, organ in enumerate(mouse.mouseOrgans):
                biodiCsvRow = completeStudy.biodiCsvRows[currRow]
                row = {
                    'Isotope': completeStudy.isotopeName,
                    'Chelator': completeStudy.chelatorName,
                    'Vector': completeStudy.vectorName,
                    'VectorType': db.getVector(completeStudy.vectorName).type,
                    'Tumor Model': completeStudy.tumorModelName,
                    'Mouse Strain': completeStudy.mouseStrainName,
                    'Mouse Gender': mouse.gender,
                    'Cage': mouse.cage,
                    'Mouse ID': mouse.mouseId,
                    'Injection Date': mouse.injectionDate,
                    'Injection Time': mouse.injectionTime,
                    'Injected Activity (kBq)': "PlaceHolder",
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
                    currWinNum = str((k + 1))
                    cpm = windowsMap[key][currRow].cpm
                    row['Dead Time Factor' + currWinNum] = "PlaceHolder"
                    row["IsotopeWin" + currWinNum] = key
                    row["Window" + currWinNum + " (counts)"] = windowsMap[key][currRow].counts
                    row["Window" + currWinNum + " corrected (counts)"] = windowsMap[key][currRow].counts
                    row["Window" + currWinNum + " (CPM)"] = cpm
                    row["Normalized Window" + currWinNum + " (CPM)"] =  "PlaceHolder"
                    row["Normalized Window" + currWinNum + " (Bq)" ] = "PlaceHolder"


                cw.writerow(row)

                currRow = currRow + 1

        file = si.getvalue()

    except BaseException as e:
        raise e

    return file, completeStudy.studyName

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
