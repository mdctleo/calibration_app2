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
from flask_jwt_extended import (
    JWTManager,
)
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
CORS(app, origins="http://localhost:8080", supports_credentials=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from calibration_app.isotope import bp as isotope_bp, Model as isotopeModel
from calibration_app.calibration import bp as calibration_bp, Model as calibrationModel
from calibration_app.counter import bp as counter_bp, Model as gammaCounterModel
from calibration_app.biodi_csv import bp as csv_bp, Model as biodiCsvCompleteModel
from statistics_app import bp as statistics_bp
from user import bp as user_bp, Model as userModel
from user.Controller import jwt

jwt.init_app(app)
app.register_blueprint(user_bp)
app.register_blueprint(isotope_bp)
app.register_blueprint(calibration_bp)
app.register_blueprint(counter_bp)
app.register_blueprint(csv_bp)
app.register_blueprint(statistics_bp)

db.create_all()
db.session.commit()
app.app_context().push()


# ----------------------------------------------------------------------------#
# Log in stuff, I failed to modularize this
# ----------------------------------------------------------------------------#

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Isotope': isotopeModel.Isotope,
            'CalibrationFactor': calibrationModel.CalibrationFactor,
            'GammaCounter': gammaCounterModel.GammaCounter,
            'User': userModel.User,
            'Protocol': biodiCsvCompleteModel.Protocol,
            'BiodiCsvRow': biodiCsvCompleteModel.BiodiCsvRow,
            'Chelator': biodiCsvCompleteModel.Chelator,
            'Vector': biodiCsvCompleteModel.Vector,
            'TumorModel': biodiCsvCompleteModel.TumorModel,
            'MouseStrain': biodiCsvCompleteModel.MouseStrain,
            'Organ': biodiCsvCompleteModel.Organ,
            'CellLine': biodiCsvCompleteModel.CellLine,
            'StudyInformation': biodiCsvCompleteModel.StudyInformation,
            'Mouse': biodiCsvCompleteModel.Mouse,
            'MouseOrgan': biodiCsvCompleteModel.MouseOrgan,
            'Window': biodiCsvCompleteModel.Window
            }



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
