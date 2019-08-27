from app import db
from calibration_app.biodi_csv.Model import Protocol, Chelator, Vector, TumorModel, MouseStrain, Organ
from calibration_app.calibration.Model import CalibrationFactor
from calibration_app.counter.Model import GammaCounter
from calibration_app.isotope.Model import Isotope
from werkzeug.security import generate_password_hash
import datetime
from user.Model import User


def populate():
    print('Got here')
    isotope1 = Isotope(isotopeName="18F", halfLife=33.3, createdBy="Carlos")
    isotope2 = Isotope(isotopeName="225Ac", halfLife=100.1, createdBy="Carlos")
    isotope3 = Isotope(isotopeName="221Fr", halfLife=200.0, createdBy="Carlos")
    isotope4 = Isotope(isotopeName="213Bi", halfLife=12.3, createdBy="Carlos")

    db.session.add(isotope1)
    db.session.add(isotope2)
    db.session.add(isotope3)
    db.session.add(isotope4)
    # db.session.commit()

    gammaCounter1 = GammaCounter(model='PE')
    gammaCounter2 = GammaCounter(model='Hidex')

    db.session.add(gammaCounter1)
    db.session.add(gammaCounter2)
    # db.session.commit()

    user = User(username="Carlos", email="carlos@bccrc.ca", password_hash=generate_password_hash("password"))

    db.session.add(user)
    # db.session.commit()

    calibrationFactor = CalibrationFactor(factor=1.1, isotopeName="225Ac", createdBy="Carlos", createdOn= datetime.datetime(2019, 8, 8), gammaCounter="Hidex")
    calibrationFactor1 = CalibrationFactor(factor=2.2, isotopeName="225Ac", createdBy="Carlos", createdOn=datetime.datetime(2019, 8, 10), gammaCounter="Hidex")
    calibrationFactor2 = CalibrationFactor(factor=1.5, isotopeName="225Ac", createdBy="Carlos", createdOn= datetime.datetime(2019, 8, 9), gammaCounter="Hidex")

    calibrationFactor3 = CalibrationFactor(factor=3.3, isotopeName="18F", createdBy="Carlos", createdOn=datetime.datetime(2019, 8, 15), gammaCounter="PE")
    calibrationFactor4 = CalibrationFactor(factor=4.2, isotopeName="18F", createdBy="Carlos", createdOn=datetime.datetime(2019, 8, 12), gammaCounter="PE")

    db.session.add(calibrationFactor)
    db.session.add(calibrationFactor2)
    db.session.add(calibrationFactor1)
    db.session.add(calibrationFactor3)
    db.session.add(calibrationFactor4)
    # db.session.commit()

    protocol = Protocol(protocolName='Test protocol')
    protocol2 = Protocol(protocolName='F-18')

    db.session.add(protocol)
    db.session.add(protocol2)
    # db.session.commit()

    chelator = Chelator(name='chelator1')
    chelator1 = Chelator(name='chelator2')

    db.session.add(chelator)
    db.session.add(chelator1)
    # db.session.commit()

    vector1 = Vector(name='vector1')
    vector2 = Vector(name='vector2')

    db.session.add(vector1)
    db.session.add(vector2)
    # db.session.commit()

    tumorModel1 = TumorModel(name='tumourModel1')
    tumorModel2 = TumorModel(name='tumorModel2')

    db.session.add(tumorModel1)
    db.session.add(tumorModel2)
    # db.session.commit()

    mouseStrain1 = MouseStrain(name='mouseStrain1')
    mouseStrain2 = MouseStrain(name='mouseStrain2')

    db.session.add(mouseStrain1)
    db.session.add(mouseStrain2)
    # db.session.commit()

    organ1 = Organ(name="Blood")
    organ2 = Organ(name="Urine")
    organ3 = Organ(name="Fat")
    organ4 = Organ(name="Seminals")

    db.session.add(organ1)
    db.session.add(organ2)
    db.session.add(organ3)
    db.session.add(organ4)

    db.session.commit()
