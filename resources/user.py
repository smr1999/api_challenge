from datetime import timedelta

from flask.views import MethodView
from flask_smorest import Blueprint,abort

from werkzeug.security import generate_password_hash, check_password_hash

from email_validator import validate_email

from schemas import UserSchema

from models import UserModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import db

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user, get_jwt

from blocklist import BLOCKLIST

blp = Blueprint("user" , __name__ , description = "'Operations on Users'")


@blp.route("/register")
class RegisterUser(MethodView):
    @blp.arguments(schema=UserSchema,
                   example={"username" : "john@gmail.com", "password": "secure_password"}
    )
    @blp.response(status_code=201)
    @blp.alt_response(status_code=400, 
                      description="When user entered invalid username format. username must have email format.",
    )
    @blp.alt_response(status_code=409,
                      description="When user wants to create account with an existing username.",
    )
    @blp.alt_response(status_code=500,
                      description="When an error in database connection and can not add this user to database.",
    )
    def post(self, user_data):
        """Register new user"""
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
                message = "An error occurred while inserting user in the database."
            )
        
        return {
            "message" : "User created successfully."
        }
    

@blp.route("/login")
class LoginUser(MethodView):
    @blp.arguments(schema=UserSchema,
                   example={"username" : "john@example.com", "password": "secure_password"},
                   description="Authenticate the user and create access_token and refresh_token."
    )
    @blp.response(status_code=200)
    @blp.alt_response(status_code=404,
                      description="If user with entered username not found.",
    )
    @blp.alt_response(status_code=400,
                      description="If user found and his/her password not valid.",
    )
    def post(self, user_data):
        """Login user and generate access_token(fresh = True) and refresh_token."""
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
        }


@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    @blp.response(status_code=200)
    def post(self):
        """Create access_token(fresh=False) based on refresh_token."""
        return {
            "access_token" : create_access_token(identity=current_user, fresh=False)
        }


@blp.route("/logout")
class LogoutUser(MethodView):
    @jwt_required()
    @blp.response(status_code=200)
    @blp.alt_response(500,
                      description="This error happen when can not connect to redis server."
    )
    def post(self):
        """Logout user and add it's access_token to blocklist(redis DB)."""
        jti = get_jwt()["jti"]
        try:
            BLOCKLIST.set( jti, "", ex=timedelta(minutes=15))
        except:
            abort(http_status_code=500,
                  message = "Redis server error."
                  )

        return {
            "message" : "successfully logged out."
        }