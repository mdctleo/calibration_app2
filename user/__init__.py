from flask import Blueprint, request

bp = Blueprint('user', __name__)

from user import Controller, Model