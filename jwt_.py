from flask import jsonify
from flask_jwt_extended import JWTManager
from app import app
jwt = JWTManager(app)

from models import UserModel

from blocklist import BLOCKLIST

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(id=identity).one_or_none()

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "message": "The token has expired.",
                "error": "token_expired"
            }
        ),
        401
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {
                "message": "Signature verification failed.", 
                "error": "invalid_token"
            }
        ),
        401
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401
    )

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = BLOCKLIST.get(jti)
    return token_in_redis is not None

@jwt.revoked_token_loader
def revoked_token_callback(wt_header, jwt_payload: dict):
    return (
        jsonify(
            {
                "description": "The token has been revoked.",
                "error": "token_revoked",
            }
        ),
        401
    )

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
        {
            "description" : "The token is not fresh.",
            "error": "fresh_token_required"
        }
        ),401
    )