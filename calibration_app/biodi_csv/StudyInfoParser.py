from calibration_app.biodi_csv.Model import StudyInformation
from datetime import datetime

def prepareStudyInformation(studyInfo, gammaInfo, protocolId, measurementTime):
    print(studyInfo['studyDate'])
    return StudyInformation(studyName=studyInfo['studyName'],
                            studyDate=datetime.strptime(studyInfo['studyDate'].split("T")[0], '%Y-%m-%d').date(),
                            researcherName=studyInfo['researcherName'],
                            piName=studyInfo['piName'],
                            isotopeName=studyInfo['radioIsotope'],
                            chelatorName=studyInfo['chelator'],
                            vectorName=studyInfo['vector'],
                            target=studyInfo['target'],
                            cellLineName=studyInfo['cellLine'],
                            mouseStrainName=studyInfo['mouseStrain'],
                            tumorModelName=studyInfo['tumorModel'],
                            radioPurity=studyInfo['radioPurity'],
                            comments=studyInfo['comments'],
                            gammaCounter=gammaInfo['gammaCounter'],
                            runDateTime= measurementTime,
                            gammaRunComments=gammaInfo['gammaCounterRunComments'],
                            protocolId=protocolId
                            )
