import os

class Api(object):
    API_TITLE = "Ad system - REST API"
    API_VERSION = "v1"

    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"

    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.25.x/"

class Database(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config(Api,Database):
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", default="jwt_secret_password")
    SECRET_KEY = os.getenv("SECRET_KEY", default="secret_password")
