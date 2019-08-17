import io
import numpy as np
from calibration_app.biodi_csv.Model import MouseOrgan, BiodiCsvRow, StudyInformation, Mouse, Window
from calibration_app.biodi_csv.DatabaseHelper import DatabaseHelper as db
from calibration_app.biodi_csv.MouseParser import *
from calibration_app.biodi_csv.StudyInfoParser import *
from exceptions.Exceptions import *
import pandas as pd

def prepareHidexWindow(row, rowNum, studyIsotope):
    try:
        windows = []
        windowHolder = {}
        for key in (row.keys()):

            if key.find("corrected (counts)") != -1:
                isotopeCounts = key.split(" ")
                if len(isotopeCounts) != 3:
                    raise IsotopeWindowParsingException("Invalid Hidex Count key")

                isotopeName = isotopeCounts[0]
                windowHolder.setdefault(isotopeName, Window())

                windowHolder[isotopeName].counts = row.get(key)

            elif key.find("Normalized") != -1 and key.find("CPM") != -1:
                isotopeCPM = key.split(" ")
                if len(isotopeCPM) != 3:
                    raise IsotopeWindowParsingException("Invalid Hidex CPM key")

                isotopeName = isotopeCPM[1]
                windowHolder.setdefault(isotopeName, Window())

                windowHolder[isotopeName].cpm = row.get(key)

        for isotopeWindow in windowHolder.items():
            if studyIsotope == '225Ac':
                isotopeWindow[1].isotopeName = isotopeWindow[0]
                isotopeWindow[1].rowNum = rowNum
                windows.append(isotopeWindow[1])
    except Exception as e:
        raise e

    return windows

def prepareHidexBiodiCsvRows(df):
    try:
        windows = []
        biodiCsvRows = []
        biodiCsvRowsDict = df.to_dict('records')
        measurementTime = biodiCsvRowsDict[0]['Time'].to_pydatetime()
        for i, row in enumerate(biodiCsvRowsDict):
            rowNum = i + 1
            biodiCsvRows.append(BiodiCsvRow(
                rowNum=rowNum,
                measurementTime=row['Time'],
                completionStatus=0,
                rack=row["Rack"],
                pos=row["Vial"],
            ))
            windows.extend(prepareHidexWindow(row, rowNum))
    except BaseException as e:
        raise e

    return biodiCsvRows, windows, measurementTime

def formatStudy(df, startRow):
    try:
        # prepare data
        df = df.truncate(before=startRow, copy=False)
        # become slicing is [closed : open]
        lastColumnIndex = df.head(1).size
        columns = df.head(1).to_numpy()[0]
        columnsAfterTags = columns[lastColumnIndex:]
        columnsToDelete = []

        for colName in columnsAfterTags:
            columnsToDelete.append(colName)

        df.drop(columnsToDelete, axis=1, inplace=True)
        # rename the columns
        df.columns = columns
        # get rid off extra row that is now the column
        df = df.truncate(before=(startRow + 1), copy=False)

        return df
    except BaseException as e:
        raise e

def parseHidexExcel(file):
    try:
        df = pd.read_excel(file)
        startRow = -1
        for row in df.itertuples():
            if (row[1] == 'Results'):
                startRow = row[0] + 1
                break


        if (startRow == -1):
            # TODO: Create an exception for this
            print("Throw an exception here")

        df = formatStudy(df, startRow)

    except Exception as e:
        raise e

    return df


def handleHidexStudy(file, studyInfo, gammaInfo, mouseInfo, organInfo):
    try:
        with db.getDb().session.no_autoflush:
            df = parseHidexExcel(file)
            mouseOrgans = assignOrgansToMouse(mouseInfo, organInfo)
            biodiCsvRows, windows, measurementTime = prepareHidexBiodiCsvRows(df)
            mice = prepareMiceAndOrgans(mouseOrgans)
            study = prepareStudyInformation(studyInfo, gammaInfo, None, measurementTime)
            study.biodiCsvRows = biodiCsvRows
            study.windows = windows
            study.mice = mice

            db.createStudy(study)
    except Exception as e:
        raise e