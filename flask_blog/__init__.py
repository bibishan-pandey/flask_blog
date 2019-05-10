from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c9e0b61b4e5c7f750d66180cdbf893d5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#create database instance
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signin'
login_manager.login_message_category = 'info'

from flask_blog import routes