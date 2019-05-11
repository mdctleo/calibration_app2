from calibration_app.calibration import bp
from flask import request
from calibration_app.calibration.Model import CalibrationFactor, CalibrationFactorSchema, DatabaseHelper as db
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError


def createCalibrationFactor(calibrationFactorDict):
    calibrationFactor = CalibrationFactor(calibrationFactorDict['factor'],
                                          calibrationFactorDict['isotopeName'],
                                          calibrationFactorDict['createdBy'],
                                          calibrationFactorDict['gammaCounter'])
    try:
        db.createCalibrationFactor(calibrationFactor)
    except IntegrityException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 400
    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    result = StandardResponse("Success")
    response = StandardResponseSchema().dump(result)
    return jsonify(response), 200


def getCalibrationFactors(model, isotopeName):
    try:
        result = db.getCalibrationFactors(model, isotopeName)
    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    response = CalibrationFactorSchema(many=True).dump(result)
    return jsonify(response), 200


@bp.route('/calibration', methods=['POST'])
# @bp.route('/calibration/<id>', methods=['GET', 'PUT', 'DELETE'])
def calibration():
    # if request.method == 'GET':
    #     return getIsotope(name)
    if request.method == 'POST':
        # TODO: createdBy should be from the authorization token, need to change this
        # TODO: implement the other REST APIs in second iteration
        try:
            calibrationFactorDict = CalibrationFactorSchema().load(request.get_json())
        except ValidationError:
            result = StandardResponse("Invaild Calibration Factor Parameters")
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400

        return createCalibrationFactor(calibrationFactorDict)
    # elif request.method == 'PUT':
    #
    #     try:
    #         newIsotopeDict = IsotopeSchema().load(request.get_json())
    #     except ValidationError:
    #         result = StandardResponse("Invaild Isotope Parameters")
    #         response = StandardResponseSchema().dump(result)
    #         return jsonify(response), 400
    #
    #     return updateIsotope(name, newIsotopeDict)
    # elif request.method == 'DELETE':
    #     return deleteIsotope(name)


@bp.route('/calibrations', methods=['GET'])
def calibrations():
    print("Got here")
    if request.method == 'GET':
        model = request.args.get('model')
        isotopeName = request.args.get('isotope')
        print(model)
        print(isotopeName)
        return getCalibrationFactors(model, isotopeName)
