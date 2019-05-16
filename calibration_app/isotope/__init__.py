from flask import Blueprint, request

bp = Blueprint('isotope', __name__)

from calibration_app.isotope import Controller, Model