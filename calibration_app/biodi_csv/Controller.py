from calibration_app.biodi_csv import bp
from flask import request
import csv
import json
from io import StringIO
from calibration_app.biodi_csv.BiodiCsvModel import BiodiCsv,  BiodiCsvRow
from calibration_app.biodi_csv.BiodiCsvCompleteModel import BiodiCsvComplete, BiodiCsvCompleteRows
from calibration_app.biodi_csv.DatabaseHelper import DatabaseHelper as db
from calibration_app.biodi_csv.Schema import BiodiCsvSchema, BiodiCsvRequestSchema
from werkzeug.utils import secure_filename
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError
from flask import make_response
from flask import Response


def prepareBiodiCsvMeta(biodiCsv):
    return BiodiCsv(biodiCsv["fileName"], biodiCsv["file"][0]["protocolId"], 'Carlos')


def prepareBiodiCsv(biodiCsv, biodiCsvId):
    biodiCsvRows = []
    csvData = biodiCsv["file"][0]
    for i, row in enumerate(csvData):
        rowNum = i + 1
        biodiCsvRows.append(BiodiCsvRow(biodiCsvId, rowNum, row["measurementTime"], row["completionStatus"],
                                        row["runId"], row["rack"], row["det"], row["pos"], row["time"],
                                        row["sampleCode"],
                                        row["counts"], row["cpm"], row["error"], row["info"]))


    return biodiCsvRows



def createBiodiCsv(biodiCsv):
    try:
        meta = prepareBiodiCsvMeta(biodiCsv)
        biodiCsvId = db.createBiodiCsv(meta)
        biodiCsvRows = prepareBiodiCsv(biodiCsv, biodiCsvId)
        db.createBiodiCsvRows(biodiCsvRows)
        return biodiCsvRows, biodiCsvId, meta.fileName
    except BaseException as e:
        raise e

def prepareBiodiCsvCompleteMeta(studyInfo, gammaInfo, biodiCsvId, biodiCsvFilename):
    BiodiCsvComplete(
        fileName=biodiCsvFilename + "_complete",
        isotope=studyInfo['radioIsotope'],

    )

    return None

def prepareBiodiCsvComplete(biodiCsvRows, biodiCsvCompleteId, mouseInfo):

    return None

def createBiodiCsvComplete(biodiCsvRows, biodiCsvId, biodiCsvFileName, studyInfo, gammaInfo, mouseInfo):
    biodiCsvCompleteMeta = prepareBiodiCsvCompleteMeta(studyInfo, gammaInfo, biodiCsvId, biodiCsvFileName)
    biodiCsvCompleteRows = prepareBiodiCsvComplete(biodiCsvRows, biodiCsvCompleteId, mouseInfo)

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
            # TODO: delegate responsibilities
            biodiCsvRows, biodiCsvId, biodiCsvFileName = createBiodiCsv(biodiCsvRequestDict['biodiCsv'])
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
