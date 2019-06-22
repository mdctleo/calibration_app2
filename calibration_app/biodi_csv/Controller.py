from calibration_app.biodi_csv import bp
from flask import request
import csv
import json
from io import StringIO
from calibration_app.biodi_csv.BiodiCsvModel import BiodiCsv,  BiodiCsvRow, DatabaseHelper as db
from calibration_app.biodi_csv.Schema import BiodiCsvSchema, BiodiCsvRowSchema, BiodiCsvRequestSchema
from werkzeug.utils import secure_filename
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError
from flask import make_response
from flask import Response




def prepareMetas(files):
    metas = []
    for file in files:
        metas.append(BiodiCsv(file["fileName"], file["file"][0]["protocolId"], 'Carlos'))

    return metas

def prepareCsvs(files, csvIds):
    biodiCsvRows = []
    for i, file in enumerate(files):
        csvData = file["file"]
        csvId = csvIds[i]
        for i, row in enumerate(csvData):
            rowNum = i + 1
            biodiCsvRows.append(BiodiCsvRow(csvId, rowNum, row["measurementTime"], row["completionStatus"],
                                        row["runId"], row["rack"], row["det"], row["pos"], row["time"], row["sampleCode"],
                                        row["counts"], row["cpm"], row["error"], row["info"]))
    return biodiCsvRows



def createCsvs(files):
    try:
        metas = prepareMetas(files)
        csvIds = db.createMetas(metas)
        biodiCsvRows = prepareCsvs(files, csvIds)
        db.createCsvs(biodiCsvRows)
    except BaseException as e:
        raise e

def getMetas():
    try:
        metas = db.getMetas()
    except BaseException as e:
        raise e

    return metas

def getCsv(csvId):
    try:
        fileName, csvRows = db.getCsv(csvId)
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
            createCsvs(biodiCsvRequestDict['files'])
        except ValidationError as e:
            result = StandardResponse("Failed to validate the CSV, please use only csv with headers:"
                                            "Protocol name, Measurement date & time, Completion status, Run ID, Rack, "
                                            "Det, Pos, Time, Sample code, * Counts, * CPM, * Error %, * Info")
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
