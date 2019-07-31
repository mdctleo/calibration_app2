from marshmallow import Schema, fields


class BaseExceptionSchema(Schema):
    msg = fields.Str()


class IntegrityException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class BaseException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class NotFoundException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class InvalidParametersException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class InvalidCredentialException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class UnauthorizedAccessException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg