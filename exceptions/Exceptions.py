from marshmallow import Schema, fields


class BaseExceptionSchema(Schema):
    message = fields.Str()


class IntegrityException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class BaseException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class NotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class InvalidParametersException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class InvalidCredentialException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message