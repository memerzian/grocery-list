from __future__ import print_function
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__,
			static_folder='client/static',
			template_folder='client/templates')

app.config.from_object(Config)
db = SQLAlchemy(app)

# Can use this to automatically generate migration scripts for the db: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
migrate = Migrate(app, db)

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes, models