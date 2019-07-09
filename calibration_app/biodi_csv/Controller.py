from calibration_app.biodi_csv import bp
from flask import request
import csv
import json
from io import StringIO
from calibration_app.biodi_csv.BiodiCsvModel import BiodiCsvRow
from calibration_app.biodi_csv.BiodiCsvCompleteModel import BiodiCsvCompleteRow, StudyInformation, Mouse
from calibration_app.biodi_csv.DatabaseHelper import DatabaseHelper as db
from calibration_app.biodi_csv.Schema import BiodiCsvSchema, BiodiCsvRequestSchema
from werkzeug.utils import secure_filename
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError
from flask import make_response
from flask import Response
import datetime



# def prepareBiodiCsvMeta(biodiCsv):
#     return BiodiCsv(biodiCsv["fileName"], biodiCsv["file"][0]["protocolId"], 'Carlos')


def prepareBiodiCsvRows(biodiCsvFile):
    biodiCsvRows = []
    protocolId = biodiCsvFile[0]['protocolId']
    for i, row in enumerate(biodiCsvFile):
        rowNum = i + 1
        biodiCsvRows.append(BiodiCsvRow(rowNum, row["measurementTime"], row["completionStatus"],
                                        row["runId"], row["rack"], row["det"], row["pos"], row["time"],
                                        row["sampleCode"],
                                        row["counts"], row["cpm"], row["error"], row["info"]))


    return biodiCsvRows, protocolId



def prepareStudyInformation(studyInfo, gammaInfo, protocolId, biodiCsvRows, biodiCsvCompleteRows, mice):
    return StudyInformation(studyName=studyInfo['studyName'],
                            studyDate=studyInfo['studyDate'],
                            researcherName =studyInfo['researcherName'],
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
                            runDateTime=biodiCsvRows[0].measurementTime,
                            gammaRunComments=gammaInfo['gammaCounterRunComments'],
                            protocolId=protocolId,
                            biodiCsvRows=biodiCsvRows,
                            biodiCsvCompleteRows=biodiCsvCompleteRows,
                            mice=mice
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


def prepareBiodiCsvCompleteRows(mouseOrgans, biodiCsvRows):
    biodiCsvCompleteRows = []
    for i, mouse in enumerate(mouseOrgans):
        for j, organ in enumerate(mouse['organs']):
            currRow = (i * j) if (i != 0) else (i + j)
            print(biodiCsvRows[currRow]['error'])
            biodiCsvCompleteRows.append(
                BiodiCsvCompleteRow(
                    rowNumber=currRow,
                    organ=organ['organ'],
                    organMass=organ['organMass'],
                    deadTimeFactor=2.2
                )
            )

    return biodiCsvCompleteRows

# def prepareWindows(biodiCsvRows):
#     windows = []
#     for i, biodiCsvRow in enumerate(biodiCsvRows):
#         windows.append(
#             Window(
#                 rowNumber=1,
#                 windowNum=1,
#             )
#         )
#
#     return windows

def prepareMice(mouseOrgans):
    mice = []
    for mouse in mouseOrgans:
        mice.append(
            Mouse(
                mouseId=mouse['mouseId'],
                groupId=mouse['groupId'],
                euthanizeDateTime=datetime.datetime.combine(mouse['euthanasiaDate'],
                                                            mouse['euthanasiaTime']),
                mouseGender=mouse['gender'],
                cage=mouse['cage'],
                age=mouse['age'],
                injectionDate=mouse['injectionDate'],
                preInjectionTime=mouse['preInjectionTime'],
                injectionTime=mouse['injectionTime'],
                postInjectionTime=mouse['postInjectionTime'],
                preInjectionActivity=mouse['preInjectionActivity'],
                postInjectionActivity=mouse['postInjectionActivity']
            )
        )

    return mice


def createStudy(biodiCsvRequestDict):
    try:

        # csvId = db.createStudyInformation(studyInformation)
        mouseOrgans = assignOrgansToMouse(biodiCsvRequestDict['mouseInfo'], biodiCsvRequestDict['organInfo'])
        biodiCsvRows, protocolId = prepareBiodiCsvRows(biodiCsvRequestDict['biodiCsv']['file'])
        biodiCsvCompleteRows = prepareBiodiCsvCompleteRows(mouseOrgans, biodiCsvRequestDict['biodiCsv']['file'])
        # windows = prepareWindows(biodiCsvRequestDict['biodiCsv']['file'])
        mice = prepareMice(mouseOrgans)

        studyInformation = prepareStudyInformation(biodiCsvRequestDict['studyInfo'],
                                                   biodiCsvRequestDict['gammaInfo'],
                                                   protocolId,
                                                   biodiCsvRows,
                                                   biodiCsvCompleteRows,
                                                   mice)

        # db.createBiodiCsvRows(biodiCsvRows)
        # db.createBiodiCsvCompleteRows(biodiCsvCompleteRows)
        # db.createMice(mice)
        # db.executeCreateStudy()
    except BaseException as e:
        raise e
    return None


def getMetas():
    try:
        metas = db.getBiodiCsvMetas()
    except BaseException as e:
        raise e

    return metas

def getCsv(csvId):
    try:
        fileName, csvRows = db.getBiodiCsv(csvId)
        si = StringIO()
        cw = csv.writer(si)
        protocolName = csvRows[0][1]
        count = protocolName + " Count"
        cpm = protocolName + " CPM"
        error = protocolName + " Error %"
        info = protocolName + " Info"
        cw.writerow(("Protocol ID", "Protocol Name", "Measurement date & time", "Completion status", "Run ID", "Rack",
                     "Det", "Pos", "Time", "Sample code", count, cpm, error, info))
        cw.writerows(csvRows)
        file = si.getvalue()

    except BaseException as e:
        raise e
    return file, fileName[0]



@bp.route('/biodicsv', methods=['POST', 'GET'])
def biodiCsv():
    if request.method == 'POST':
        try:
            biodiCsvRequestDict = BiodiCsvRequestSchema().load(request.get_json())
            createStudy(biodiCsvRequestDict)
        except ValidationError as e:
            result = StandardResponse(e.__str__())
            # result = StandardResponse("Failed to validate the CSV, please use only csv with headers:"
            #                                 "Protocol name, Measurement date & time, Completion status, Run ID, Rack, "
            #                                 "Det, Pos, Time, Sample code, * Counts, * CPM, * Error %, * Info")
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
            result, fileName = getCsv(request.args.get('id'))
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400
        except Exception as e:
            print(e.__str__())
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

        response = make_response(result)
        response.headers["Content-Disposition"] = "attachment; filename=" + fileName
        response.headers["Content-Type"] = "test/csv; charset=UTF-8"
        return response, 200



@bp.route('/biodicsv-metas', methods=['GET'])
def biodiCsvMetas():
    if request.method == 'GET':
        try:
            result = getMetas()
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

        response = BiodiCsvSchema(many=True).dump(result)
        return jsonify(response), 200
