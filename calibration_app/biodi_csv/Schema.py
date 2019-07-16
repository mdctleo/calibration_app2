from marshmallow import Schema, fields, INCLUDE


class ProtocolSchema(Schema):
    name = fields.Str(required=True, max_length=8)


class StudyInformationMetaSchema(Schema):
    id = fields.Integer(required=True)
    studyName = fields.Str(required=True)
    researcherName = fields.Str(required=True)
    createdOn = fields.DateTime(required=True)


class BiodiCsvRowSchema(Schema):
    class Meta:
        unknown = INCLUDE

    rowNum = fields.Int(dump_only=True)
    protocolId = fields.Integer(data_key="Protocol ID", required=True)
    protocolName = fields.Str(dump_only=True)
    measurementTime = fields.DateTime(data_key='Measurement date & time', required=True)
    completionStatus = fields.Int(data_key='Completion status')
    runId = fields.Int(data_key='Run ID')
    rack = fields.Int(data_key='Rack')
    det = fields.Int(data_key='Det')
    pos = fields.Int(data_key='Pos')
    time = fields.Float(data_key='Time')
    sampleCode = fields.Str(data_key='Sample code', max_length=45)
    # counts = fields.Float(data_key='Counts')
    # cpm = fields.Float(data_key='CPM')
    # error = fields.Float(data_key='Error %')
    # info = fields.Str(data_key='Info', max_length=1)


class BiodiCsvFileSchema(Schema):
    fileName = fields.Str(required=True)
    file = fields.Nested(BiodiCsvRowSchema, many=True)


class StudyInfoSchema(Schema):
    studyName = fields.Str(required=True)
    studyDate = fields.DateTime(required=True)
    researcherName = fields.Str(required=True)
    piName = fields.Str(required=True)
    radioIsotope = fields.Str(required=True)
    chelator = fields.Str(required=True)
    vector = fields.Str(required=True)
    target = fields.Str(required=True)
    cellLine = fields.Str(required=True)
    mouseStrain = fields.Str(required=True)
    tumorModel = fields.Str(required=True)
    radioPurity = fields.Float(required=True)
    comments = fields.Str()


class GammaInfoSchema(Schema):
    gammaCounter = fields.Str(required=True)
    gammaCounterRunTimeOffset = fields.Str()
    gammaCounterRunComments = fields.Str()


class MouseCsvRowSchema(Schema):
    mouseId = fields.Str(data_key="Mouse ID", required=True)
    gender = fields.Str(data_key="Gender", required=True)
    cage = fields.Str(data_key="Cage", required=True)
    age = fields.Number(data_key="Age", required=True)
    groupId = fields.Str(data_key="Group ID", required=True)
    euthanasiaDate = fields.Date(data_key="Euthanasia Date", required=True)
    euthanasiaTime = fields.Time(data_key="Euthanasia Time", required=True)
    weight = fields.Float(data_key="Weight (g)", required=True)
    injectionDate = fields.Date(data_key="Injection Date", required=True)
    preInjectionTime = fields.Time(data_key="Pre-Injection Time", require=True)
    injectionTime = fields.Time(data_key="Injection Time", require=True)
    postInjectionTime = fields.Time(data_key="Post-Injection Time", require=True)
    preInjectionActivity = fields.Float(data_key="Pre-Injection MBq", reuqire=True)
    postInjectionActivity = fields.Float(data_key="Post-Injection MBq", require=True)
    comments = fields.Str(data_key="Comments")


class OrganSchema(Schema):
    organ = fields.Str(required=True)
    organMass = fields.Float(required=True)


class OrganInfoSchema(Schema):
    organs = fields.Nested(OrganSchema, many=True)
    groupId = fields.Str(required=True)
    mouseId = fields.Str(required=True)


class BiodiCsvRequestSchema(Schema):
    biodiCsv = fields.Nested(BiodiCsvFileSchema)
    studyInfo = fields.Nested(StudyInfoSchema)
    gammaInfo = fields.Nested(GammaInfoSchema)
    mouseInfo = fields.Nested(MouseCsvRowSchema, many=True)
    organInfo = fields.Nested(OrganInfoSchema, many=True)
