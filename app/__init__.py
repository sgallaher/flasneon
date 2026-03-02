from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = "auth.login"

def create_app():
   app = Flask(__name__)
   app.config.from_object(Config)

   db.init_app(app)
   login_manager.init_app(app)
   migrate.init_app(app, db)

   # Register blueprints
   from .auth.routes import auth
   from .main.routes import main

   app.register_blueprint(auth)
   app.register_blueprint(main)

   return app
