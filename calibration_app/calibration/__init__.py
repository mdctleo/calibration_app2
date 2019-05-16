from flask import Blueprint, request

bp = Blueprint('calibration', __name__)


from calibration_app.calibration import Controller, Model