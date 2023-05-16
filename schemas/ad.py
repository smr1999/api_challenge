from marshmallow import Schema, fields


class PlainAdSchema(Schema):
    id = fields.Integer(dump_only = True)
    title = fields.String(required=True)
    description = fields.String(required=True)

class AdSchema(PlainAdSchema):
    from .user import PlainUserSchema
    creator = fields.Nested(PlainUserSchema, dump_only=True)