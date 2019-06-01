from calibration_app.calibration import bp
from flask import request
from calibration_app.calibration.Model import CalibrationFactor, CalibrationFactorSchema, CalibrationFactorGraphSchema, DatabaseHelper as db
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError
from constants.CommonModel import PlotlyTrace, PlotlyGraph, PlotlyGraphSchema


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

def getCalibrationFactorsGraph(model, isotopeName):
    try:
        results = db.getCalibrationFactorsGraph(model, isotopeName)
        isotopeMap = {}
        for calibrationFactor in results:
            if not calibrationFactor.isotopeName in isotopeMap:
                isotopeMap[calibrationFactor.isotopeName] = [[], []]
                isotopeMap[calibrationFactor.isotopeName][0].append(calibrationFactor.createdOn)
                isotopeMap[calibrationFactor.isotopeName][1].append(calibrationFactor.factor)
            else:
                isotopeMap[calibrationFactor.isotopeName][0].append(calibrationFactor.createdOn)
                isotopeMap[calibrationFactor.isotopeName][1].append(calibrationFactor.factor)

        graph = []
        for isotope, values in isotopeMap.items():
            graph.append(PlotlyTrace(mode='lines+markes', name=isotope, x=values[0], y=values[1]))

        graph = PlotlyGraph(graph)
        print(graph)

    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    response = PlotlyGraphSchema().dump(graph)
    print(response)
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
    if request.method == 'GET':
        model = request.args.get('model')
        isotopeName = request.args.get('isotope')
        return getCalibrationFactors(model, isotopeName)

@bp.route('/calibrations/graph', methods=['GET'])
def calibrationsGraph():
    if request.method == 'GET':
        model = request.args.get('model')
        isotopeName = request.args.get('isotope')
        if model is None:
            # Graphs need at least a model selected
            result = StandardResponse("Graphs need at least a model selected")
            response = StandardResponseSchema().dump(result)
            # 200 so it does not trigger an error response in the frontend, no graph would be plotted
            return jsonify(response), 204
        return getCalibrationFactorsGraph(model, isotopeName)

