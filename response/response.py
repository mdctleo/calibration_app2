from marshmallow import Schema, fields


class StandardResponse:
    def __init__(self, message):
        self.message = message


class StandardResponseSchema(Schema):
    message = fields.Str()
