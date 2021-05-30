from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import secret

app = Flask(__name__)
app.secret_key = secret.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import views

