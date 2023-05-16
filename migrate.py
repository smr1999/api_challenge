from flask_migrate import Migrate

from app import app
from db import db
migrate = Migrate(app,db)