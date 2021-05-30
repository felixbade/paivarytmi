from flask import Flask

import secret

app = Flask(__name__)
app.secret_key = secret.secret_key

from app import views

