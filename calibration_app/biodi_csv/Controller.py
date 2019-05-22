from calibration_app.biodi_csv import bp
from flask import request
import csv
import json
import os
from calibration_app.biodi_csv.Model import BiodiCsv, BiodiCsvRequestSchema, DatabaseHelper as db
from werkzeug.utils import secure_filename
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError


def prepareMetas(files):
    metas = []
    for file in files:
        metas.append(BiodiCsv(file['fileName'], file['file'][0]['protocolId']))

    return 'Not Implemented'

def prepareCsvs(csvData):
    return 'Not Implemented'


def createCsvs(files):
    try:
        metas = prepareMetas(files)

    except IntegrityException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 400
    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    result = StandardResponse("Success")
    response = StandardResponseSchema().dump(result)
    return jsonify(response), 200


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

        return "Got Here"
    elif request.method == 'GET':

        return "Not Implemented"