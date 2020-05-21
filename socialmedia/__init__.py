from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '222997886598bf047d5bd0fabb518b583900433e6f284448ffa1b5e60201a35e'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///socialmedia.db'

db = SQLAlchemy(app)

from socialmedia import routes
