from flask.views import MethodView
from flask_smorest import Blueprint,abort

from werkzeug.security import generate_password_hash

from email_validator import validate_email

from schemas import UserSchema

from models import UserModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import db

blp = Blueprint("user" , __name__ , description = "User blueprint")


@blp.route("/register")
class RegisterUser(MethodView):
    @blp.arguments(schema=UserSchema)
    def post(self, user_data):
        try:
            validate_email(user_data["username"])
        except:
            abort(
                http_status_code=400,
                message = "Invalid Username format. Format must have email format.",
            )

        try:
            user = UserModel(
                username = user_data["username"],
                password = generate_password_hash(password=user_data["password"])
            )
            db.session.add(user)
            db.session.commit()
        
        except IntegrityError:
            db.session.rollback()
            abort(
                http_status_code=409,
                message = "User with this username exists."
            )
        
        except SQLAlchemyError:
            db.session.rollback()
            abort(
                http_status_code=500,
                message = "An error occurred while inserting user in the database. "
            )
        
        return {
            "message" : "User created successfully."
        }, 201