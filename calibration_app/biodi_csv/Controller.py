from flask_jwt_extended import jwt_required
from flask_login import login_required

from calibration_app.biodi_csv import bp
from flask import request
import csv
from io import StringIO
from calibration_app.biodi_csv.Model import MouseOrgan, BiodiCsvRow, StudyInformation, Mouse, Window
from calibration_app.biodi_csv.DatabaseHelper import DatabaseHelper as db
from calibration_app.biodi_csv.Schema import BiodiCsvRequestSchema, StudyInformationMetaSchema, ChelatorSchema, \
    VectorSchema, CellLineSchema, MouseStrainSchema, TumorModelSchema
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError
from flask import make_response
import datetime


def prepareBiodiCsvRows(biodiCsvFile):
    biodiCsvRows = []
    protocolId = biodiCsvFile[0]['protocolId']
    for i, row in enumerate(biodiCsvFile):
        rowNum = i + 1
        biodiCsvRows.append(BiodiCsvRow(
                                        rowNum=rowNum,
                                        measurementTime=row["measurementTime"],
                                        completionStatus=row["completionStatus"],
                                        runId=row["runId"],
                                        rack=row["rack"],
                                        det=row["det"],
                                        pos=row["pos"],
                                        time=row["time"],
                                        sampleCode=row["sampleCode"]
                                        ))


    return biodiCsvRows, protocolId


def prepareStudyInformation(studyInfo, gammaInfo, protocolId, measurementTime):
        return StudyInformation(studyName=studyInfo['studyName'],
                                studyDate=studyInfo['studyDate'],
                                researcherName=studyInfo['researcherName'],
                                piName=studyInfo['piName'],
                                isotopeName=studyInfo['radioIsotope'],
                                chelatorName=studyInfo['chelator'],
                                vectorName=studyInfo['vector'],
                                target=studyInfo['target'],
                                cellLineName=studyInfo['cellLine'],
                                mouseStrainName=studyInfo['mouseStrain'],
                                tumorModelName=studyInfo['tumorModel'],
                                radioPurity=studyInfo['radioPurity'],
                                comments=studyInfo['comments'],
                                gammaCounter=gammaInfo['gammaCounter'],
                                runDateTime=measurementTime,
                                gammaRunComments=gammaInfo['gammaCounterRunComments'],
                                protocolId=protocolId
                                )

def assignOrgansToMouse(mouseInfo, organInfo):
    mouseOrgans = []
    for i, organObject in enumerate(organInfo):
        for i, mouseObject in enumerate(mouseInfo):
            if (mouseObject['mouseId'] == organObject['mouseId']):
                mouseObject['organs'] = organObject['organs']
                mouseOrgans.append(mouseObject)
                break

    return mouseOrgans

def prepareWindows(biodiCsvRows):
    try:
        windows = []
        for rowNum, row in enumerate(biodiCsvRows):
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
                isotopeWindow[1].isotopeName = isotopeWindow[0]
                isotopeWindow[1].rowNum = rowNum
                windows.append(isotopeWindow[1])


    except Exception as e:
        raise e

    return windows

def prepareMiceAndOrgans(mouseOrgans):
    mice = []
    for mouse in mouseOrgans:
        mouseHolder = Mouse(
            mouseId=mouse['mouseId'],
            groupId=mouse['groupId'],
            euthanizeDateTime=datetime.datetime.combine(mouse['euthanasiaDate'],
                                                        mouse['euthanasiaTime']),
            gender=mouse['gender'],
            cage=mouse['cage'],
            age=mouse['age'],
            injectionDate=mouse['injectionDate'],
            preInjectionTime=mouse['preInjectionTime'],
            injectionTime=mouse['injectionTime'],
            postInjectionTime=mouse['postInjectionTime'],
            preInjectionActivity=mouse['preInjectionActivity'],
            postInjectionActivity=mouse['postInjectionActivity']
        )
        for organ in mouse['organs']:
            mouseHolder.mouseOrgans.append(
                MouseOrgan(
                    organName=organ['organ'],
                    organMass=organ['organMass']
                )
            )
        mice.append(mouseHolder)

    return mice

def createStudy(biodiCsvRequestDict):
    try:

        with db.getDb().session.no_autoflush:
            mouseOrgans = assignOrgansToMouse(biodiCsvRequestDict['mouseInfo'], biodiCsvRequestDict['organInfo'])
            biodiCsvRows, protocolId = prepareBiodiCsvRows(biodiCsvRequestDict['biodiCsv']['file'])
            mice = prepareMiceAndOrgans(mouseOrgans)
            windows = prepareWindows(biodiCsvRequestDict['biodiCsv']['file'])
            study = prepareStudyInformation(biodiCsvRequestDict['studyInfo'],
                                            biodiCsvRequestDict['gammaInfo'],
                                            biodiCsvRequestDict['biodiCsv']['file'][0]['protocolId'],
                                            biodiCsvRequestDict['biodiCsv']['file'][0]['measurementTime'])
            study.biodiCsvRows = biodiCsvRows
            study.windows = windows
            study.mice = mice
    #
            db.createStudy(study)
    except BaseException as e:
        raise e
    return None


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

def createCompleteStudyRow(biodiCsvRow, mouse, organ):

    return None

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
                createCompleteStudyRow(biodiCsvRow, mouse, organ)
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
                    deadTimeFactor = windowsMap[key][currRow].error
                    cpm = windowsMap[key][currRow].cpm
                    row['Dead Time Factor' + currWinNum] = deadTimeFactor
                    row["IsotopeWin" + currWinNum] = key
                    row["Window" + currWinNum + " (counts)"] = windowsMap[key][currRow].counts
                    row["Window" + currWinNum + " corrected (counts)"] = cpm / deadTimeFactor
                    row["Window" + currWinNum + " (CPM)"] = cpm
                    row["Normalized Window" + currWinNum + " (CPM)"] = "PlaceHolder"
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

@bp.route('/biodicsv', methods=['POST', 'GET'])
def biodiCsv():
    if request.method == 'POST':
        try:
            biodiCsvRequestDict = BiodiCsvRequestSchema().load(request.get_json())
            createStudy(biodiCsvRequestDict)
        except ValidationError as e:
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

        result = StandardResponse("Success")
        response = StandardResponseSchema().dump(result)
        return jsonify(response), 200
    elif request.method == 'GET':
        try:
            result, studyName = getCompleteStudy(request.args.get('id'))
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema.dump(result)
            return jsonify(response), 500

        response = make_response(result)
        response.headers["Content-Disposition"] = "attachment; filename=" + studyName
        response.headers["Content-Type"] = "text/csv; charset=UTF-8"

        return response, 200

@bp.route('/biodicsv-raw')
def biodiCsvRaw():
    if request.method == 'GET':
        try:
            result, studyName = getBiodiCsvRaw(request.args.get('id'))
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema.dump(result)
            return jsonify(response), 500

        response = make_response(result)
        response.headers["Content-Disposition"] = "attachment; filename=" + studyName
        response.headers["Content-Type"] = "text/csv; charset=UTF-8"

        return response, 200



@bp.route('/biodicsv-metas', methods=['GET'])
@jwt_required
def biodiCsvMetas():
    print(request)
    if request.method == 'GET':
        try:
            result = getMetas()
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

        response = StudyInformationMetaSchema(many=True).dump(result)
        return jsonify(response), 200

@bp.route('/chelators', methods=['GET'])
def chelators():
    if request.method == 'GET':
        try:
            result = getChelators()
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema.dump(result)
            return jsonify(response), 500

        response = ChelatorSchema(many=True).dump(result)
        return jsonify(response), 200

@bp.route('/vectors', methods=['GET'])
def vectors():
    if request.method == 'GET':
        try:
            result = getVectors()
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema.dump(result)
            return jsonify(response), 200

        response = VectorSchema(many=True, exclude=['type']).dump(result)
        return jsonify(response), 200

@bp.route('/cell-lines', methods=['GET'])
def cellLines():
    if request.method == 'GET':
        try:
            result = getCellLines()
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema.dump(result)
            return jsonify(response), 200

        response = CellLineSchema(many=True).dump(result)
        return jsonify(response), 200

@bp.route('/mouse-strains', methods=['GET'])
def mouseStrains():
    if request.method == 'GET':
        try:
            result = getMouseStrains()
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema.dump(result)
            return jsonify(response), 200

        response = MouseStrainSchema(many=True).dump(result)
        return jsonify(response), 200

@bp.route('/tumor-models', methods=['GET'])
def tumorModels():
    if request.method == 'GET':
        try:
            result = getTumorModels()
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema.dump(result)
            return jsonify(response), 200

        response = TumorModelSchema(many=True).dump(result)
        return jsonify(response), 200
    return None
