from biodi import app_biodi,db
from biodi.models import User,Isotope,BioDi

@app_biodi.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Isotope': Isotope,'BioDi':BioDi}