from calibration_app.biodi_csv import bp
from flask import request
from marshmallow import ValidationError
from flask import jsonify
from flask_jwt_extended import jwt_required
from calibration_app.biodi_csv.Schema import BiodiCsvRequestSchema, StudyInformationMetaSchema, ChelatorSchema, \
    VectorSchema, CellLineSchema, MouseStrainSchema, TumorModelSchema
from response.response import StandardResponse, StandardResponseSchema
from flask import make_response
from calibration_app.biodi_csv.Controller import *
from calibration_app.biodi_csv.HidexParser import *
from calibration_app.biodi_csv.MouseParser import *
import pandas as pd
import json


@bp.route('/biodicsv', methods=['POST', 'GET'])
@jwt_required
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
@jwt_required
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
    if request.method == 'GET':
        try:
            result = getMetas()
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

        response = StudyInformationMetaSchema(many=True).dump(result)
        return make_response(jsonify(response), 200)

@bp.route('/chelators', methods=['GET'])
@jwt_required
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
@jwt_required
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
@jwt_required
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
@jwt_required
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
@jwt_required
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

@bp.route('/biodicsv-test', methods=['POST'])
@jwt_required
def biodiCsvTest():
    if request.method =='POST':
        print(request)
        print(request.files)
        print(request.get_json())
        # studyInfo = json.load(request.files['studyInfo'])
        # gammaInfo = json.load(request.files['gammaInfo'])
        mouseInfo = pd.read_json(request.files['mouseInfo'])
        organInfo = json.load(request.files['organInfo'])
        biodiFile = request.files['biodiFile']
        print(mouseInfo)

        # if gammaInfo['gammaCounter'] == "Hidex":
        #     handleHidexStudy(biodiFile,studyInfo, gammaInfo, mouseInfo, organInfo)

        # print(request.files)
        # hidex = request.files['hidex']
        # mouseCsv = request.files['mouseCsv']
        # organCsv = request.files['organCsv']
        return "Success", 200