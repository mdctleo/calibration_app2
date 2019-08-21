from numpy import exp,log


def calculateDecay(activity, tref, t2, halfLife):
    # deltaT = (t2.hour - tref.hour) * 60 + t2.minute - tref.minute + (t2.second - tref.second) / 60.0
    deltaT = t2 - tref
    deltaT = deltaT.total_seconds() / 60.0
    activityDecayed = activity * exp(-(log(2) / halfLife) * deltaT)

    return activityDecayed

'''
Args:
    cpm (int): normalized cpm
    halfLife (float): half-life of study's isotope
    tref (datetime): injection time of mouse
    t (datetime): measurement time of the first tube
    calibrationFactor (float): most recent calibration factor of the isotope on the study's gamma counter
    
Returns:
    mouseActivity (float): calibrated activity of mouse

'''

def calculateCalibratedMouseActivity(cpm, halfLife, tref, t, calibrationFactor):
    deltaT = t - tref
    deltaT = deltaT.total_seconds() / 60.0
    print(deltaT)
    mouseActivity = cpm * exp((log(2) / halfLife) * deltaT) * calibrationFactor
    return mouseActivity
