from db import db


class CommentModel(db.Model):
    __tablename__ = "comments"

    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), primary_key = True)
    ad_id = db.Column(db.Integer(), db.ForeignKey("ads.id"), primary_key = True)

    comment = db.Column(db.String(), nullable=False)