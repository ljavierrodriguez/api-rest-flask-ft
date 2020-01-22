import os
from flask import Flask, render_template, jsonify, request, Blueprint
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager
)

from models import db, Category, User, Post
from routes.category import route_categories
from routes.user import route_users
from routes.auth import auth
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True 
app.config['ENV'] = 'development' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3)
CORS(app)
jwt = JWTManager(app)
db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)



@app.route('/')
def home():
    return render_template('index.html', name='home')

app.register_blueprint(auth)
app.register_blueprint(route_categories, url_prefix='/api')
app.register_blueprint(route_users, url_prefix='/api')


if __name__ == '__main__':
    manager.run()