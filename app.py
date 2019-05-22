# from biodi import app_biodi,db
# from biodi.models import User,Isotope,BioDi
# from calibration_app import app_calibration
#
# @app_biodi.shell_context_processor
# def make_shell_context():
#     return {'BioDiDB': db, 'User': User, 'Isotope': Isotope,'BioDi':BioDi}

# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from sqlalchemy.engine import Engine
from sqlalchemy import event
# TODO: remove CORS, we dont really need it for production
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager
import os

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#


app = Flask(__name__)
app.config.from_object('config')
# TODO: Adjust the allowed origins for better security?
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

from routes import *
from user import Model as userModel
from calibration_app.isotope import bp as isotope_bp, Model as isotopeModel
from calibration_app.calibration import bp as calibration_bp, Model as calibrationModel
from calibration_app.counter import bp as counter_bp, Model as gammaCounterModel
from calibration_app.biodi_csv import bp as csv_bp, Model as biodiCsvModel

app.register_blueprint(isotope_bp)
app.register_blueprint(calibration_bp)
app.register_blueprint(counter_bp)
app.register_blueprint(csv_bp)

db.create_all()
db.session.commit()
app.app_context().push()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Isotope': isotopeModel.Isotope, 'CalibrationFactor': calibrationModel.CalibrationFactor,
            'GammaCounter': gammaCounterModel.GammaCounter, 'User': userModel.User, 'Protocol': biodiCsvModel.Protocol,
            'BiodiCsv': biodiCsvModel.BiodiCsv, 'BiodiCsvRow': biodiCsvModel.BiodiCsvRow}



# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
