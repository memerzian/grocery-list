from __future__ import print_function
from flask import Flask

app = Flask(__name__,
			static_folder='client/static',
			template_folder='client/templates')

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes