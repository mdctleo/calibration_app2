from calibration_app.counter import bp
from flask import request
from calibration_app.counter.Model import GammaCounter, GammaCounterSchema, DatabaseHelper as db
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError


def getCounters():
    try:
        result = db.getCounters()
    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    response = GammaCounterSchema(many=True).dump(result)
    return jsonify(response), 200


def createCounter(counterDict):
    gammaCounter = GammaCounter(counterDict['model'])
    try:
        result = db.createCounter(gammaCounter)
    except IntegrityException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 400
    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    result = StandardResponse("Success")
    response = StandardResponseSchema().dump(result)
    return jsonify(response), 200


@bp.route('/counter', methods=['POST'])
# @bp.route('/isotope/<name>', methods=['GET', 'PUT', 'DELETE'])
def counter():
    # if request.method == 'GET':
    #     return getIsotope(name)
    if request.method == 'POST':
        # TODO: implement rest of API
        try:
            counterDict = GammaCounterSchema().load(request.get_json())
        except ValidationError:
            result = StandardResponse("Invaild counter Parameters")
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400

        return createCounter(counterDict)
    # elif request.method == 'PUT':
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


@bp.route('/counters', methods=['GET'])
def counters():
    if request.method == 'GET':
        return getCounters()
