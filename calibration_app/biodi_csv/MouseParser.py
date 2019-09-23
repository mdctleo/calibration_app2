from calibration_app.biodi_csv.Model import MouseOrgan, Mouse
from exceptions.Exceptions import *
from datetime import datetime

def handleMouseOrganCsv():
    
    return None

def handleMouseCsv(mouseCsv):

    return None


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
            euthanizeDateTime=datetime.strptime(mouse['Euthanasia Date'] + ' ' + mouse['Euthanasia Time'], '%Y-%m-%d %H:%M:%S'),
            gender=mouse['Gender'],
            cage=mouse['Cage'],
            age=mouse['Age'],
            injectionDate=datetime.strptime(mouse['Injection Date'], '%Y-%m-%d').date(),
            preInjectionTime=datetime.strptime(mouse['Pre-Injection Time'], '%H:%M:%S').time(),
            injectionTime=datetime.strptime(mouse['Injection Time'], '%H:%M:%S').time(),
            postInjectionTime=datetime.strptime(mouse['Post-Injection Time'], '%H:%M:%S').time(),
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