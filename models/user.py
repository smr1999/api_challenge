from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique = True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    ads = db.relationship("AdModel", backref = "creator", lazy= "dynamic", cascade= "all,delete")
    comments = db.relationship("CommentModel", backref = "writer", lazy= "dynamic", cascade= "all,delete")