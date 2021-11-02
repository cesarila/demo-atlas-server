from flask_migrate import Migrate
from app import create_app, db
from app.models import *
from app.api import *
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)