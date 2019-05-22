from calibration_app.biodi_csv import bp
from flask import request
import csv
import json
import os
from calibration_app.biodi_csv.Model import BiodiCsv, BiodiCsvRow, BiodiCsvRequestSchema, DatabaseHelper as db
from werkzeug.utils import secure_filename
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError


def prepareMetas(files):
    metas = []
    for file in files:
        metas.append(BiodiCsv(file["fileName"], file["file"][0]["protocolId"]))

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


@bp.route('/biodicsv', methods=['POST', 'GET'])
def biodicsv():
    if request.method == 'POST':
        try:
            biodiCsvRequestDict = BiodiCsvRequestSchema().load(request.get_json())
            createCsvs(biodiCsvRequestDict['files'])
        except ValidationError as e:
            result = StandardResponse("Failed to validate the CSV, please use only csv with headers:"
                                            "Protocol name, Measurement date & time, Completion status, Run ID, Rack, "
                                            "Det, Pos, Time, Sample code, * Counts, * CPM, * Error %, % Info")
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400
        except BaseException as e:
            response = StandardResponseSchema().dump(e)
            return jsonify(response), 500

        result = StandardResponse("Success")
        response = StandardResponseSchema().dump(result)
        return jsonify(response), 200
    elif request.method == 'GET':

        return "Not Implemented"