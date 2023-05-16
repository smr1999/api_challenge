from db import db


class AdModel(db.Model):
    __tablename__ = "ads"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(), nullable=False)

    creator_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)