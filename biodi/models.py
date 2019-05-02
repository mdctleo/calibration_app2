from biodi import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Isotope(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    isotope_name = db.Column(db.String(32),index=True,unique=True)
    half_life = db.Column(db.Float(32))
    hidex_calfactor = db.Column(db.Float(32))
    wizard_calfactor = db.Column(db.Float(32))
    cal_factor_date = db.Column(db.DateTime,index=True,)
    bio_data = db.relationship('BioDi',backref='biodata',lazy='dynamic')

    def __repr__(self):
        return '<Isotope {}>'.format(self.isotope_name)

class BioDi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpm = db.Column(db.Integer)
    isotope_id = db.Column(db.Integer,db.ForeignKey('isotope.id'))

    def __repr__(self):
        return '<BioDi {}>'.format(self.id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))