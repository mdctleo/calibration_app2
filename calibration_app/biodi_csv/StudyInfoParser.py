from calibration_app.biodi_csv.Model import StudyInformation
import pandas as pd
def prepareStudyInformation(studyInfo, gammaInfo, protocolId, measurementTime):
    return StudyInformation(studyName=studyInfo['studyName'],
                            studyDate=studyInfo['studyDate'],
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
                            runDateTime= pd.to_datetime(measurementTime),
                            gammaRunComments=gammaInfo['gammaCounterRunComments'],
                            protocolId=protocolId
                            )
