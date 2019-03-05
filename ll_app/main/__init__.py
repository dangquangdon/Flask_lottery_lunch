from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

import os

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'adm.admin_login'
login_manager.login_message_category = 'warning'

bcrypt = Bcrypt()



def create_app(config_type):
    app = Flask(__name__)

    configuration = os.path.join(os.getcwd(), 'config', config_type+'.py')

    app.config.from_pyfile(configuration)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)


    from main.subscribers import subs
    from main.admin_user import adm


    app.register_blueprint(subs)
    app.register_blueprint(adm)

    return app
