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
        print(metas)
    except BaseException as e:
        raise e

    return metas

def getBiodiCsvRaw(studyId):
    try:
        completeStudy, isotope, calibrationFactor = db.getCompleteStudy(studyId)
        windowsMap = createWindowsMap(completeStudy.windows)
        si = StringIO()
        fieldnames = []
        if completeStudy.protocolId is not None:
            fieldnames.append("Protocol ID")
            fieldnames.append("Protocol name")

        fieldnames.append("Measurement date & time")
        fieldnames.append("Completion status")
        fieldnames.append("Run ID")
        fieldnames.append("Rack")
        fieldnames.append("Det")
        fieldnames.append("Pos")
        fieldnames.append("Time")
        fieldnames.append("Sample code")

        for i, key in enumerate(windowsMap.keys()):
            fieldnames.append(key + " Counts")
            fieldnames.append(key + " Error %")
            fieldnames.append(key + " CPM")
            fieldnames.append(key + " Info")

        cw = csv.DictWriter(si, fieldnames=fieldnames)
        cw.writeheader()
        currRow=0

        for i, row in enumerate(completeStudy.biodiCsvRows):
            csvRow = {}
            completionStatus = row.completionStatus
            if completeStudy.protocolId is not None:
                csvRow["Protocol ID"] = completeStudy.protocolId,
                csvRow["Protocol name"] = db.getProtocolName(completeStudy.protocolId),
            # csvRow["Measurement date & time"] = row.measurementTime,
            csvRow.update({"Measurement date & time": row.measurementTime})
            csvRow.update({"Completion status": completionStatus}),
            csvRow.update({"Run ID": row.runId}),
            csvRow.update({"Rack": row.rack}),
            csvRow.update({"Det": row.det}),
            csvRow.update({"Pos": row.pos}),
            csvRow.update({"Time": row.time}),
            csvRow.update({"Sample code": row.sampleCode})

            for i, key in enumerate(windowsMap.keys()):
                csvRow[key + " Counts"] = windowsMap[key][currRow].counts
                csvRow[key + " Error %"] = windowsMap[key][currRow].error
                csvRow[key + " CPM"] = windowsMap[key][currRow].cpm
                csvRow[key + " Info"] = windowsMap[key][currRow].info

            cw.writerow(csvRow)

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
                    row["Window " + currWinNum + " %ID/g @ injectionTime"] = ((mouseAcitivty / injectedActivity) * 100) / organ.organMass





                cw.writerow(row)

                currRow = currRow + 1

        file = si.getvalue()
    except BaseException as e:
        raise e

    return file, completeStudy.studyName

def getStudyAnalysis(studyId):
    completeStudyCsv, studyName = getCompleteStudy(studyId)
    studyPd = pd.read_csv(StringIO(completeStudyCsv))
    columnsToSlice = []
    for column in studyPd.columns:
        if column.find("%ID/g @ injectionTime") != -1:
            columnsToSlice.append(column)
    columnsToSlice.append("Organ")
    columnsToSlice.append("TimePoint (h)")
    studyPd = studyPd[columnsToSlice]
    csv = studyPd.groupby(['Organ', 'TimePoint (h)']).describe().to_csv()
    return csv, studyName

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
