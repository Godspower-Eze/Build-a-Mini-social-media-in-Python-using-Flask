from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '222997886598bf047d5bd0fabb518b583900433e6f284448ffa1b5e60201a35e'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///socialmedia.db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

login_manager.login_view = 'login'

login_manager.login_message_category = 'info'

from socialmedia import routes
