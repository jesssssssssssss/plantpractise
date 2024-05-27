from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

# NEW ADDITIONS ^^^

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'random key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(app.root_path, DB_NAME)}' #
    db.init_app(app) # NEW ADDITIONS < ^ 

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # NEW ADDITIONS vv

    from .models import User, Product, AccountDetails

    create_database(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # NEW ADDITIONS end

    return app

def create_database(app): #NEW ADDITION vv
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Database created!")