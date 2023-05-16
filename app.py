from flask import Flask
from flask_smorest import Api

from config import Config

app = Flask(__name__)

app.config.from_object(Config)

api = Api(app)