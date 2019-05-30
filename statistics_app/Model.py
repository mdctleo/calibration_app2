from marshmallow import Schema, fields

class StatisticFormSchema(Schema):
    input0 = fields.Float()
    input1 = fields.Float()
    alpha = fields.Float()
    test = fields.Str()
    alternative = fields.Str()

class StatisticFormResponseSchema(Schema):
    result = fields.Float()