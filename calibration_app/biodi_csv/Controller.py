from calibration_app.biodi_csv import bp
from flask import request
import csv
import json
from io import StringIO
from calibration_app.biodi_csv.BiodiCsvModel import BiodiCsvRow
from calibration_app.biodi_csv.BiodiCsvCompleteModel import BiodiCsvCompleteRow
from calibration_app.biodi_csv.DatabaseHelper import DatabaseHelper as db
from calibration_app.biodi_csv.Schema import BiodiCsvSchema, BiodiCsvRequestSchema
from werkzeug.utils import secure_filename
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError
from flask import make_response
from flask import Response


# def prepareBiodiCsvMeta(biodiCsv):
#     return BiodiCsv(biodiCsv["fileName"], biodiCsv["file"][0]["protocolId"], 'Carlos')


def prepareBiodiCsvRows(biodiCsv, biodiCsvId):
    biodiCsvRows = []
    csvData = biodiCsv["file"][0]
    for i, row in enumerate(csvData):
        rowNum = i + 1
        biodiCsvRows.append(BiodiCsvRow(biodiCsvId, rowNum, row["measurementTime"], row["completionStatus"],
                                        row["runId"], row["rack"], row["det"], row["pos"], row["time"],
                                        row["sampleCode"],
                                        row["counts"], row["cpm"], row["error"], row["info"]))


    return biodiCsvRows



def prepareStudyInformation(studyInfo, gammaInfo, biodiCsvId, biodiCsvFilename):

    return None

def prepareBiodiCsvCompleteRows(biodiCsvRows, csvId, mouseInfo, organInfo):
    # biodiCsvRowsCompleteRows = []
    # for i, row in enumerate(biodiCsvRows):
    #     for i, row in enumerate(mouseInfo):
    #         for

    # biodiCsvCompleteRows = []
    # for i, row in enumerate(biodiCsvRows):
    #     rowNum = i +1
    #     biodiCsvCompleteRows.append(BiodiCsvCompleteRow(
    #         rowNumber=rowNum,
    #         csvId=csvId,
    #         mouseGender= mouseInfo[i].gender,
    #
    #     ))


    return None

def createBiodiCsvComplete(biodiCsvRequestDict):
    try:
        studyInformation = prepareStudyInformation(biodiCsvRequestDict['studyInfo'],
                                                   biodiCsvRequestDict['gammaInfo'],
                                                   biodiCsvRequestDict['mouseInfo'])
        csvId = db.createStudyInformation(studyInformation)
        biodiCsvRows = prepareBiodiCsvRows(biodiCsvRequestDict['biodiCsv'], csvId)
        db.createBiodiCsvRows(biodiCsvRows)
        biodiCsvCompleteRows = prepareBiodiCsvCompleteRows(biodiCsvRows, csvId,
                                                           biodiCsvRequestDict['mouseInfo'],
                                                           biodiCsvRequestDict['organInfo'])
        db.createBiodiCsvCompleteRows(biodiCsvCompleteRows)
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
            print(biodiCsvRequestDict)
            createBiodiCsvComplete(biodiCsvRequestDict)
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
