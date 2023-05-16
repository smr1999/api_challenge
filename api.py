from flask_smorest import Api

from app import app
api = Api(app)

from resources import UserBlueprint
api.register_blueprint(UserBlueprint)