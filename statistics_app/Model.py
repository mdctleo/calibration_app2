from marshmallow import Schema, fields

class StatisticFormSchema(Schema):
    effect = fields.Float()
    nobs = fields.Float()
    power = fields.Float()
    alpha = fields.Float()
    test = fields.Str()
    alternative = fields.Str()

class StatisticFormResponseSchema(Schema):
    result = fields.Float()