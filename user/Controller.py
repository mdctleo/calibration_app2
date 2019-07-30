from flask_jwt_extended.exceptions import JWTExtendedException

from user.Model import DatabaseHelper as db, UserSchema
from flask import request, make_response
from response.response import StandardResponse, StandardResponseSchema
from flask import jsonify
from marshmallow import ValidationError
from user import bp
from exceptions.Exceptions import *
from flask_jwt_extended import (
    create_access_token,
    get_raw_jwt,
    jwt_required, JWTManager)

jwt = JWTManager()
blacklist = set()

def loginHelper(email, password):
        user = db.getUser(email)
        if user is None or not user.check_password(password):
            raise InvalidCredentialException("Invalid login credentials")

        token = create_access_token(user.email)
        return {'token': token}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    print(blacklist)
    return jti in blacklist

def logoutHelper():
    try:
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
    except Exception as e:
        raise BaseException(e.__str__())



@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            userDict = UserSchema().load(request.get_json())
            result = loginHelper(userDict['email'], userDict['password'])
        except ValidationError as e:
            result = StandardResponse(e.__str__())
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 400
        except InvalidCredentialException as e:
            result = StandardResponseSchema(e.message)
            response = StandardResponseSchema.dump(result)
            return jsonify(response), 401
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

    response = UserSchema().dump(result)
    return jsonify(response), 200

@bp.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    if request.method == 'DELETE':
        try:
            logoutHelper()
        except BaseException as e:
            result = StandardResponse(e.message)
            response = StandardResponseSchema().dump(result)
            return jsonify(response), 500

        result = StandardResponse("success")
        response = StandardResponseSchema().dump(result)
        return jsonify(response), 200