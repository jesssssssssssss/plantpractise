from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
DB_NAME = "database.db"

#Initialise Mail instance
mail = Mail()

def create_app(mail_instance=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'random key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(app.root_path, DB_NAME)}' 
    db.init_app(app) 
    
    #Configuring Flask-Mail for Outlook
    app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com' #Where outlook emails are hosted from
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'SendUsFeedback@outlook.com'
    app.config['MAIL_PASSWORD'] = 'plantsRawesome'
    

    if mail_instance:
        mail_instance.init_app(app)
    else:
        global mail
        mail.init_app(app)

    #Importing blueprints
    from .views import views
    from .auth import auth
    from .routes import bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(bp, url_prefix='/contact')

    from .models import User, Product, AccountDetails, ShopProducts

    create_database(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app, mail

def create_database(app): 
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Database checked/updated with new tables!")