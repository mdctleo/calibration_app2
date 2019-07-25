
from user.Model import DatabaseHelper as db, UserSchema
from flask import request
from response.response import StandardResponse, StandardResponseSchema
from flask import jsonify
from marshmallow import ValidationError
from user import bp
from exceptions.Exceptions import *
from flask_jwt_extended import (
create_access_token
)

def loginHelper(email, password):
        user = db.getUser(email)
        if user is None or not user.check_password(password):
            raise InvalidCredentialException("Invalid login credentials")

        token = create_access_token(user.email)
        return {'token': token}


@bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        print("Got here")
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
    print(response)
    return jsonify(response), 200