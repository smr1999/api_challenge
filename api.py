from flask_smorest import Api

from app import app
api = Api(app)

from resources import UserBlueprint, AdBlueprint
api.register_blueprint(UserBlueprint)
api.register_blueprint(AdBlueprint)