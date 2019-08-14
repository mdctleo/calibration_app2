from calibration_app.biodi_csv.Model import MouseOrgan, Mouse
from exceptions.Exceptions import *
import datetime


def assignOrgansToMouse(mouseInfo, organInfo):
    mouseOrgans = []
    for i, organObject in enumerate(organInfo):
        for i, mouseObject in enumerate(mouseInfo):
            if (mouseObject['Mouse ID'] == organObject['mouseId']):
                mouseObject['organs'] = organObject['organs']
                mouseOrgans.append(mouseObject)
                break

    return mouseOrgans

def prepareMiceAndOrgans(mouseOrgans):
    mice = []
    for mouse in mouseOrgans:
        mouseHolder = Mouse(
            mouseId=mouse['Mouse ID'],
            groupId=mouse['Group ID'],
            euthanizeDateTime=datetime.datetime.combine(mouse['Euthanasia Date'],
                                                        mouse['Euthanasia Time']),
            gender=mouse['Gender'],
            cage=mouse['Cage'],
            age=mouse['Age'],
            injectionDate=mouse['Injection Date'],
            preInjectionTime=mouse['Pre-Injection Time'],
            injectionTime=mouse['Injection Time'],
            postInjectionTime=mouse['Post-Injection Time'],
            preInjectionActivity=mouse['Pre-Injection MBq'],
            postInjectionActivity=mouse['Post-Injection MBq']
        )
        for organ in mouse['organs']:
            mouseHolder.mouseOrgans.append(
                MouseOrgan(
                    organName=organ['organ'],
                    organMass=organ['organMass']
                )
            )
        mice.append(mouseHolder)

    return mice