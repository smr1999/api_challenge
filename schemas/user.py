from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Int(required=True, dump_only = True)
    username = fields.Str(required=True, load_only=True)
    password = fields.Str(required=True, load_only=True)

class UserSchema(PlainUserSchema):
    from .ad import PlainAdSchema
    ads = fields.List(fields.Nested(PlainAdSchema), required=True, dump_only=True)