from calibration_app.biodi_csv import bp
from flask import request
import csv
import json
import os
from calibration_app.biodi_csv.Model import BiodiCsv, DatabaseHelper as db
from werkzeug.utils import secure_filename
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError



def createCsvs(csvs):
    try:
        result = db.createCsvs(csvs)
    except IntegrityException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 400
    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    result = StandardResponse("Success")
    response = StandardResponseSchema().dump(result)
    return jsonify(response), 200


@bp.route('/csv', methods=['POST', 'GET'])
def csv():
    if request.method == 'POST':
        print(request.get_json())


        return "Got Here"
    elif request.method == 'GET':

        return "Not Implemented"