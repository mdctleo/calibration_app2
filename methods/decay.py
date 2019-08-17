from numpy import exp,log


def calculateDecay(activity, tref, t2, halfLife):
    # deltaT = (t2.hour - tref.hour) * 60 + t2.minute - tref.minute + (t2.second - tref.second) / 60.0
    deltaT = t2 - tref
    deltaT = deltaT.total_seconds() / 60.0
    activityDecayed = activity * exp(-(log(2) / halfLife) * deltaT)

    return activityDecayed

