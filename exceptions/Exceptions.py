from marshmallow import Schema, fields


class BaseExceptionSchema(Schema):
    payload = fields.Str()


class IntegrityException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.payload = message


class BaseException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.payload = message


class NotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.payload = message

class InvalidParametersException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.payload = message