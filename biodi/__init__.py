from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# from flask_debugtoolbar import DebugToolbarExtension

app_biodi = Flask(__name__)
app_biodi.debug = True
app_biodi.config.from_object(Config)
db = SQLAlchemy(app_biodi)
migrate = Migrate(app_biodi, db)
login = LoginManager(app_biodi)
login.login_view = 'login'

from biodi import routes, models#, statistics
# from biodi.methods import statistics