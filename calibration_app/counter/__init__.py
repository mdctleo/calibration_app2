from flask import Blueprint, request

bp = Blueprint('counter', __name__)

from calibration_app.counter import Controller, Model