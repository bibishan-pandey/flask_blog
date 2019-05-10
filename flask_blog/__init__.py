from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c9e0b61b4e5c7f750d66180cdbf893d5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#create database instance
db = SQLAlchemy(app)

from flask_blog import routes