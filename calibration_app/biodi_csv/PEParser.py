from calibration_app.biodi_csv.DatabaseHelper import DatabaseHelper as db
from calibration_app.biodi_csv.MouseParser import *
from calibration_app.biodi_csv.StudyInfoParser import *
from calibration_app.biodi_csv.Model import BiodiCsvRow, Window
from exceptions.Exceptions import *
import numpy as np
import pandas as pd

def preparePEWindow(row, rowNum, studyIsotope):
    try:
        windows = []
        windowHolder = {}
        for key in (row.keys()):
            if (key.find("Counts") != -1):
                isotopeCounts = key.split(" ")

                if (len(isotopeCounts) != 2):
                    raise BaseException("Invalid counts key")

                isotopeName = isotopeCounts[0]
                windowHolder.setdefault(isotopeName, Window())

                windowHolder[isotopeName].counts = row.get(key)

            elif (key.find("Error %") != -1):
                isotopeError = key.split(" ")

                if (len(isotopeError) != 3):
                    raise BaseException("Invalid Error % key")

                isotopeName = isotopeError[0]
                windowHolder.setdefault(isotopeName, Window())

                windowHolder[isotopeName].error = row.get(key)

            elif (key.find("CPM") != -1):
                isotopeCPM = key.split(" ")

                if (len(isotopeCPM) != 2):
                    raise BaseException("Invalid CPM key")

                isotopeName = isotopeCPM[0]
                windowHolder.setdefault(isotopeName, Window())

                windowHolder[isotopeName].cpm = row.get(key)

            elif (key.find("Info") != -1):
                isotopeInfo = key.split(" ")

                if (len(isotopeInfo) != 2):
                    raise BaseException("Invalid Info key")

                isotopeName = isotopeInfo[0]
                windowHolder.setdefault(isotopeName, Window())

                windowHolder[isotopeName].info = row.get(key)

        for isotopeWindow in windowHolder.items():
            isotopeWindow[1].isotopeName = isotopeNameReplace(isotopeWindow[0], studyIsotope)
            isotopeWindow[1].rowNum = rowNum
            windows.append(isotopeWindow[1])


    except Exception as e:
        raise e

    return windows

def isotopeNameReplace(isotopeName, studyIsotope):
    try:
        if studyIsotope != '225Ac':
            elementNumberArr = isotopeName.split("-")
            replacement = elementNumberArr[1] + elementNumberArr[0]
        else:
            windowIsotopeName = isotopeName.split("_")[0]

            firstOccurenceNumber = -1
            for i, c in enumerate(windowIsotopeName):
                if c.isnumeric():
                    firstOccurenceNumber = i
                    break

            replacement = windowIsotopeName[firstOccurenceNumber: len(windowIsotopeName)] \
                          + windowIsotopeName[0: firstOccurenceNumber]

            print(replacement)


    except Exception as e:
        raise e

    return replacement


def preparePEBiodiCsvRows(df, studyIsotope):
    try:
        biodiCsvFile = df.to_dict('records')
        print(biodiCsvFile)
        biodiCsvRows = []
        windows = []
        protocolId = biodiCsvFile[0]['Protocol ID']
        measurementTime = datetime.strptime(biodiCsvFile[0]['Measurement date & time'], '%Y-%m-%d %H:%M:%S')
        for i, row in enumerate(biodiCsvFile):
            rowNum = i + 1
            biodiCsvRows.append(BiodiCsvRow(
                rowNum=rowNum,
                measurementTime=datetime.strptime(row["Measurement date & time"],'%Y-%m-%d %H:%M:%S' ),
                completionStatus=row["Completion status"],
                runId=row["Run ID"],
                rack=row["Rack"],
                det=row["Det"],
                pos=row["Pos"],
                time=row["Time"],
                sampleCode=row["Sample code"]
            ))
            windows.extend(preparePEWindow(row, rowNum, studyIsotope))
    except BaseException as e:
        raise e

    return biodiCsvRows, windows, protocolId, measurementTime


def parsePECsv(file):
    try:
        df = pd.read_csv(file)
    except Exception as e:
        raise e

    return df

def handlePEStudy(file, studyInfo, gammaInfo, mouseInfo, organInfo):
    try:
        with db.getDb().session.no_autoflush:
            df = parsePECsv(file)
            mouseOrgans = assignOrgansToMouse(mouseInfo, organInfo)
            biodiCsvRows, windows, protocolId, measurementTime = preparePEBiodiCsvRows(df, studyInfo['radioIsotope'])
            mice = prepareMiceAndOrgans(mouseOrgans)
            study = prepareStudyInformation(studyInfo, gammaInfo, protocolId, measurementTime)
            study.biodiCsvRows = biodiCsvRows
            study.windows = windows
            study.mice = mice

            db.createStudy(study)
    except Exception as e:
        raise e