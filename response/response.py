from marshmallow import Schema, fields


class StandardResponse:
    def __init__(self, message):
        self.payload = message


class StandardResponseSchema(Schema):
    payload = fields.Str()
