from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '222997886598bf047d5bd0fabb518b583900433e6f284448ffa1b5e60201a35e'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///socialmedia.db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from socialmedia import routes
