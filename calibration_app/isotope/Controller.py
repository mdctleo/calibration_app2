from calibration_app.isotope import bp
from flask import request
from calibration_app.isotope.Model import Isotope, IsotopeSchema, DatabaseHelper as db
from flask import jsonify
from response.response import StandardResponse, StandardResponseSchema
from exceptions.Exceptions import *
from marshmallow import ValidationError


def getIsotopes():
    try:
        result = db.getIsotopes()
    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    response = IsotopeSchema(many=True).dump(result)
    return jsonify(response), 200


def getIsotope(name):
    try:
        result = db.getIsotope(name)
    except NotFoundException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 400
    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    response = IsotopeSchema().dump(result)
    return jsonify(response), 200


def createIsotope(isotopeDict):
    isotope = Isotope(isotopeDict['isotopeName'], isotopeDict['halfLife'], isotopeDict['createdBy'])
    try:
        result = db.createIsotope(isotope)
    except IntegrityException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 400
    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    result = StandardResponse("Success")
    response = StandardResponseSchema().dump(result)
    return jsonify(response), 200


def updateIsotope(name, newIsotopeDict):
    newIsotope = Isotope(newIsotopeDict['isotopeName'], newIsotopeDict['halfLife'], newIsotopeDict['createdBy'])

    try:
        isotopeToUpdate = db.getIsotope(name)
        db.updateIsotope(isotopeToUpdate, newIsotope, newIsotope.createdBy)
    except NotFoundException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 400
    except IntegrityException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 400
    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    result = StandardResponse("Success")
    response = StandardResponseSchema().dump(result)
    return jsonify(response), 200


def deleteIsotope(name):
    try:
        isotopeToDelete = db.getIsotope(name)
        db.deleteIsotope(isotopeToDelete)
    except NotFoundException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 400
    except BaseException as e:
        response = BaseExceptionSchema().dump(e)
        return jsonify(response), 500

    result = StandardResponse("Success")
    response = StandardResponseSchema().dump(result)
    return jsonify(response), 200


@bp.route('/isotope', methods=['POST'], defaults={'name': None})
@bp.route('/isotope/<name>', methods=['GET', 'PUT', 'DELETE'])
def isotope(name):
    if request.method == 'GET':
        return getIsotope(name)
    elif request.method == 'POST':
        # TODO: createdBy should be from the authorization token, need to change this
        try:
            isotopeDict = IsotopeSchema().load(request.get_json())
        except ValidationError:
            result = StandardResponse("Invaild Isotope Parameters")
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400

        return createIsotope(isotopeDict)
    elif request.method == 'PUT':
        # TODO: createdBy should be from the authorization token, need to change this
        try:
            newIsotopeDict = IsotopeSchema().load(request.get_json())
        except ValidationError:
            result = StandardResponse("Invaild Isotope Parameters")
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400

        return updateIsotope(name, newIsotopeDict)
    elif request.method == 'DELETE':
        return deleteIsotope(name)


@bp.route('/isotopes', methods=['GET'])
def isotopes():
    if request.method == 'GET':
        return getIsotopes()
