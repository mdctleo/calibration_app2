from marshmallow import Schema, fields


class ProtocolSchema(Schema):
    name = fields.Str(required=True, max_length=8)


class BiodiCsvSchema(Schema):
    id = fields.Integer()
    fileName = fields.Str()
    protocolId = fields.Integer()
    createdOn = fields.DateTime()
    createdBy = fields.Str()


class BiodiCsvRowSchema(Schema):
    rowNum = fields.Int(dump_only=True)
    protocolId = fields.Integer(data_key="Protocol ID")
    protocolName = fields.Str(dump_only=True)
    measurementTime = fields.DateTime(data_key='Measurement date & time')
    completionStatus = fields.Int(data_key='Completion status')
    runId = fields.Int(data_key='Run ID')
    rack = fields.Int(data_key='Rack')
    det = fields.Int(data_key='Det')
    pos = fields.Int(data_key='Pos')
    time = fields.Float(data_key='Time')
    sampleCode = fields.Str(data_key='Sample code', max_length=45)
    counts = fields.Float(data_key='Counts')
    cpm = fields.Float(data_key='CPM')
    error = fields.Float(data_key='Error %')
    info = fields.Str(data_key='Info', max_length=1)


class BiodiCsvFileSchema(Schema):
    fileName = fields.Str(required=True)
    file = fields.Nested(BiodiCsvRowSchema, many=True)


class StudyInfoSchema(Schema):
    studyName = fields.Str(required=True)
    studyDate = fields.Date(required=True)
    researcherName = fields.Str(required=True)
    piName = fields.Str(required=True)
    radioIsotope = fields.Str(required=True)
    chelator = fields.Str(required=True)
    vector = fields.Str(required=True)
    target = fields.Str(required=True)
    cellLine = fields.Str(required=True)
    radioActivity = fields.Float(required=True)
    radioPurity = fields.Float(required=True)
    comments = fields.Str()


class GammaInfoSchema(Schema):
    gammaCounter = fields.Str(required=True)
    gammaCounterRunDateTime = fields.DateTime(required=True)
    gammaCounterRunTimeOffset = fields.Str()
    gammaCounterRunComments = fields.Str()


class MouseCsvRowSchema(Schema):
    mouseId = fields.Str(required=True)
    gender = fields.Str(required=True)
    groupId = fields.Str(required=True)
    weight = fields.Float(required=True)
    injectionDate = fields.Date(required=True)
    preInjectionTime = fields.Time(require=True)
    injectionTime = fields.Time(require=True)
    postInjectionTime = fields.Time(require=True)
    preInjectionActivity = fields.Float(reuqire=True)
    postInjectionActivity = fields.Float(require=True)
    comments = fields.Str()


class OrganSchema(Schema):
    organ = fields.Str(required=True)


class BiodiCsvRequestSchema(Schema):
    biodiCsv = fields.Nested(BiodiCsvFileSchema)
    studyInfo = fields.Nested(StudyInfoSchema)
    gammaInfo = fields.Nested(GammaInfoSchema)
    mouseInfo = fields.Nested(MouseCsvRowSchema, many=True)
    organInfo = fields.Nested(OrganSchema, many=True)
