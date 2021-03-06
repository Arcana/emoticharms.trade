from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
import steam

app = Flask(__name__, instance_relative_config=True, static_folder='build')
app.config.from_object('settings')
app.config.from_pyfile('settings.py')

# Setup debugtoolbar, if we're in debug mode.
if app.debug:
    from flask.ext.debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)

# Flask extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
oid = OpenID(app)

# Setup steamodd
steam.api.key.set(app.config['STEAM_API_KEY'])
steam.api.socket_timeout.set(5)

# Views
import views

# Blueprints
from .users.views import users as users_blueprint
from .emoticharms.views import emoticharms as emoticharms_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(emoticharms_blueprint)
