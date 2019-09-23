from marshmallow import Schema, fields, INCLUDE


class ProtocolSchema(Schema):
    name = fields.Str(required=True, max_length=8)

class ChelatorSchema(Schema):
    name = fields.Str()

class VectorSchema(Schema):
    name = fields.Str()
    type = fields.Str()

class TumorModelSchema(Schema):
    name = fields.Str()

class MouseStrainSchema(Schema):
    name = fields.Str()

class CellLineSchema(Schema):
    name = fields.Str()


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


class BiodiCsvFileSchema(Schema):
    fileName = fields.Str(required=True)
    file = fields.Nested(BiodiCsvRowSchema, many=True)


class StudyInfoSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    studyName = fields.Str(required=True)
    studyDate = fields.DateTime(required=True)
    researcherName = fields.Str(required=True)
    piName = fields.Str(required=True)
    isotopeName = fields.Str(required=True)
    chelatorName = fields.Str(required=True)
    vectorName = fields.Str(required=True)
    target = fields.Str(required=True)
    mouseStrainName = fields.Str(required=True)
    tumorModelName = fields.Str(required=True)
    radioPurity = fields.Float(required=True)
    gammaCounter = fields.Str(required=True, dump_only=True)
    numGammaRuns = fields.Integer(required=True, load_only=True)
    comment = fields.Str()


class GammaInfoSchema(Schema):
    gammaCounter =fields.Str(required=True)
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
