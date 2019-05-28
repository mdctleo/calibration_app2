from flask import Blueprint, request

bp = Blueprint('statistics', __name__)

from statistics_app import Controller