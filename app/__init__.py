from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '5623'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:placeholder@localhost:5432/postgres'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

from app import routes

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
