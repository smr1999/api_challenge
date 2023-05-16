from flask_smorest import Api

from app import app
api = Api(app)

from resources import UserBlueprint, AdBlueprint, CommentBlueprint
api.register_blueprint(UserBlueprint)
api.register_blueprint(AdBlueprint)
api.register_blueprint(CommentBlueprint)