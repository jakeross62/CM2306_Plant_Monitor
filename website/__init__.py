from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e4ab0da0a722d9db0b73fcaa53bfb57acb018860c6cf3331'

# suppress SQLAlchemy warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# get abs path to the app dir to create the db here
basedir = os.path.abspath(os.path.dirname(__file__))

# Creating db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'website.db')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from website import routes

with app.app_context():
   db.create_all()
