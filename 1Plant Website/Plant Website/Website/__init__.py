from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
DB_NAME = "database.db"

# NEW ADDITIONS ^^^

mail = Mail()

def create_app(mail_instance=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'random key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(app.root_path, DB_NAME)}' #
    db.init_app(app) # NEW ADDITIONS < ^ 
    
    if mail_instance:
        mail_instance.init_app(app) #Initialise the Mail instance with the app
    else:
        mail = Mail(app) #Create a new Mail instance if one is not provided

    #Importing blueprints
    from .views import views
    from .auth import auth
    from .routes import bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(bp, url_prefix='/contact')

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

    return app, mail

def create_database(app): #NEW ADDITION vv
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Database created!")