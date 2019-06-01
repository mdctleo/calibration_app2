from marshmallow import Schema, fields


class PlotlyTraceSchema(Schema):
    mode = fields.Str()
    name = fields.Str()
    type = fields.Str()
    x = fields.List(fields.Float())
    y = fields.List(fields.Float())

class PlotlyGraphSchema(Schema):
    data = fields.List(fields.Nested(PlotlyTraceSchema))

class PlotlyTrace():
    def __init__ (self, mode, name, x, y, type=None):
        self.mode = mode
        self.name = name
        self.type = type
        self.x = x
        self.y = y

    def __repr__(self):
        return "<PolyTrace %r %r %r %r %r>" % (self.mode, self.name, self.type, self.x, self.y)

class PlotlyGraph():
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return "<PolyGrpah %r>" % self.data