from marshmallow import Schema, fields

class PlainCommentSchema(Schema):
    from .user import PlainUserSchema
    writer = fields.Nested(PlainUserSchema, dump_only=True)
    comment = fields.String(required=True)

class CommentSchema(PlainCommentSchema):
    from .user import PlainUserSchema
    writer = fields.Nested(PlainUserSchema, dump_only=True)

    from .ad import PlainAdSchema
    ad = fields.Nested(PlainAdSchema, dump_only=True)