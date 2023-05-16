from datetime import timedelta

from flask.views import MethodView
from flask_smorest import Blueprint,abort

from werkzeug.security import generate_password_hash, check_password_hash

from email_validator import validate_email

from schemas import UserSchema

from models import UserModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import db

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user, get_jti

from blocklist import BLOCKLIST

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
    

@blp.route("/login")
class LoginUser(MethodView):
    @blp.arguments(schema=UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(username = user_data["username"]).first()

        if not user:
            abort(
                http_status_code=404,
                message="User with this username not found."
            )
        
        if not check_password_hash(user.password, user_data["password"]):
            abort(
                http_status_code=400,
                message="Invalid password."
            )
        
        access_token = create_access_token(identity=user, fresh=True)
        refresh_token = create_refresh_token(identity=user)

        return {
            "access_token" : access_token,
            "refresh_token" : refresh_token
        }, 200


@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        return {
            "access_token" : create_access_token(identity=current_user, fresh=False)
        }, 200


@blp.route("/logout")
class LogoutUser(MethodView):
    @jwt_required()
    def post(self):
        BLOCKLIST.set( get_jti(), "", ex=timedelta(minutes=15))

        return {
            "message" : "successfully logged out."
        }, 200