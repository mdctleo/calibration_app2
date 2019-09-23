from calibration_app.biodi_csv.Model import StudyInformation, GammaCounterRun
from datetime import datetime

def prepareStudyInformation(studyInfo):
    return StudyInformation(studyName=studyInfo['studyName'],
                            studyDate=studyInfo['studyDate'],
                            researcherName=studyInfo['researcherName'],
                            piName=studyInfo['piName'],
                            isotopeName=studyInfo['isotopeName'],
                            chelatorName=studyInfo['chelatorName'],
                            vectorName=studyInfo['vectorName'],
                            target=studyInfo['target'],
                            mouseStrainName=studyInfo['mouseStrainName'],
                            tumorModelName=studyInfo['tumorModelName'],
                            radioPurity=studyInfo['radioPurity'],
                            comments=studyInfo['comment']
                            )

    # runId = db.Column(GAMMA_COUNTER_RUN_C_RUN_ID, db.SmallInteger, nullable=False)
    # studyName = db.Column(GAMMA_COUNTER_RUN_STUDY_NAME, db.String, db.ForeignKey(STUDY_INFORMATION_T_NAME + '.' + STUDY_INFORMATION_C_STUDY_NAME), nullable=False)
    # gammaCounter = db.Column(GAMMA_COUNTER_RUN_C_GAMMA_COUNTER, db.String(8), db.ForeignKey(GAMMA_COUNTERS_T_NAME + '.' + GAMMA_COUNTERS_C_MODEL), nullable=False)
    # protocolId = db.Column(GAMMA_COUNTER_RUN_C_PROTOCOL_ID, db.Integer, db.ForeignKey(PROTOCOL_T_NAME + '.' + PROTOCOL_C_ID))
    # runDateTime = db.Column(STUDY_INFORMATION_C_RUN_DATE_TIME, db.DateTime, nullable=False)
    # gammaRunComments = db.Column(STUDY_INFORMATION_C_GAMMA_RUN_COMMENTS, db.Text)

def prepareGammaRunInformation(gammaInfoDict, runId, protocolId, measurementTime):
    return GammaCounterRun(runId=runId,
                           gammaCounter=gammaInfoDict['gammaCounter'],
                           protocolId=protocolId,
                           runDateTime=measurementTime,
                           gammaRunComments=gammaInfoDict['gammaCounterRunComments']
                           )

    return None